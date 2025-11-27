import re
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from io import BytesIO
import os
from itertools import product
import requests

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"

# ========= REGEX CURP =========
CURP_RE = re.compile(
    r"(?<![A-Z0-9])"
    r"([A-Z][AEIOUX][A-Z]{2}\d{2}"
    r"(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])"
    r"[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)"
    r"[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)"
    r"(?![A-Z0-9])"
)

KEYWORDS_STRONG = [
    "INSTITUTO NACIONAL ELECTORAL",
    "CREDENCIAL PARA VOTAR",
    "CLAVE DE ELECTOR",
    "CURP",
]

KEYWORDS_MED = [
    "DOMICILIO",
    "SECCION", "SECCIÓN",
    "VIGENCIA",
    "AÑO DE REGISTRO", "ANO DE REGISTRO",
    "FECHA DE NACIMIENTO", "FECHA NACIMIENTO",
    "SEXO",
]

RED_FLAGS = [
    "NO ES UNA INE REAL",
    "FINES DE PRUEBA",
    "MUESTRA",
    "SAMPLE",
    "DEMO",
]

# etiquetas OCR
LABEL_CURP_OR_ANIO = re.compile(
    r"(?:\bCURP\b|A(?:Ñ|N)O\s*DE\s*REGISTRO|A(?:Ñ|N)O\s*DEREGISTRO|A(?:Ñ|N)ODEREGISTRO)",
    re.IGNORECASE
)
LABEL_CLAVE_ELECTOR_ANY = re.compile(
    r"(?:CLAVE\s*DE\s*ELECTOR|CLAVE\s*DEELECTOR|CLAVEDE\s*ELECTOR|CLAVEDEELECTOR)",
    re.IGNORECASE
)
LABEL_ANIO_REG = re.compile(
    r"(?:A(?:Ñ|N)O\s*DE\s*REGISTRO|A(?:Ñ|N)O\s*DEREGISTRO|A(?:Ñ|N)ODEREGISTRO)",
    re.IGNORECASE
)
LABEL_CURP_ONLY = re.compile(r"\bCURP\b", re.IGNORECASE)

# Clave elector
CLAVE_ELECTOR_RE = re.compile(r"^[A-Z]{6}\d{6}\d{2}[HM]\d{3}$")


# ---------- helpers de texto ----------
def normalize(s: str) -> str:
    return " ".join((s or "").upper().split())


def clean_alnum(s: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


# ---------- lectura PDF ----------
def extract_text_embedded(pdf_bytes: bytes, max_pages=2) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    parts = []
    for i in range(min(max_pages, doc.page_count)):
        parts.append(doc.load_page(i).get_text("text") or "")
    return "\n".join(parts)


# ---------- OCR ----------
def preprocess_variants(img: Image.Image) -> list[Image.Image]:
    variants = []

    g = img.convert("L")
    variants.append(g)

    g1 = ImageEnhance.Contrast(g).enhance(2.0)
    variants.append(g1)

    g2 = ImageOps.autocontrast(g)
    variants.append(g2)

    def thresh(im, t=160):
        return im.point(lambda p: 255 if p > t else 0)

    variants.append(thresh(g2, 150))
    variants.append(thresh(g2, 170))

    g3 = ImageEnhance.Contrast(ImageOps.grayscale(img)).enhance(2.5)
    variants.append(thresh(g3, 160))

    return variants


def ocr_image(img: Image.Image, lang="spa") -> str:
    config = "--oem 3 --psm 6"
    return pytesseract.image_to_string(img, lang=lang, config=config)


def analyze_ine_score_only(text_raw: str) -> int:
    t = normalize(text_raw)
    score = 0
    for k in KEYWORDS_STRONG:
        if k in t:
            score += 4
    for k in KEYWORDS_MED:
        if k in t:
            score += 1

    if CURP_RE.search(re.sub(r"[^A-Z0-9\s]", " ", t)):
        score += 4
    if "CLAVE" in t and "ELECTOR" in t:
        score += 2
    if any(rf in t for rf in RED_FLAGS):
        score -= 10
    return score


def ocr_first_pages_best(pdf_bytes: bytes, max_pages=2, dpi_scale=4) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    best_text = ""
    best_score = -999

    for i in range(min(max_pages, doc.page_count)):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi_scale, dpi_scale), alpha=False)
        base_img = Image.open(BytesIO(pix.tobytes("png")))

        for vimg in preprocess_variants(base_img):
            try:
                txt = ocr_image(vimg, lang="spa")
            except Exception:
                txt = ocr_image(vimg, lang="eng")

            s = analyze_ine_score_only(txt)
            if s > best_score:
                best_score = s
                best_text = txt

    return best_text


# ---------- extracción CURP / clave ----------
def extract_after_label(text: str, label_re: re.Pattern, max_capture: int = 200) -> str | None:
    t = normalize(text)
    m = label_re.search(t)
    if not m:
        return None
    tail = t[m.end(): m.end() + max_capture]
    return clean_alnum(tail) or None


def generate_curp_variants(curp18: str, max_variants: int = 2500) -> list[str]:
    s = curp18.upper()
    if len(s) != 18:
        return []

    letter_pos = {0, 1, 2, 3, 11, 12, 13, 14, 15}
    digit_pos = {4, 5, 6, 7, 8, 9, 17}

    subs_digit = {
        "O": ["0"],
        "Q": ["0"],
        "D": ["0"],
        "I": ["1"],
        "L": ["1"],
        "S": ["8", "5"],
        "B": ["8"],
        "Z": ["2"],
        "G": ["6"],
        "T": ["7"],
        "A": ["4"],
        "8": ["9", "8"],
        "9": ["8", "9"],
    }
    subs_letter = {
        "0": ["O"],
        "1": ["I"],
        "2": ["Z"],
        "5": ["S"],
        "8": ["B"],
    }

    options = []
    for i, ch in enumerate(s):
        opts = [ch]

        if i in digit_pos and ch in subs_digit:
            opts = list(dict.fromkeys(opts + subs_digit[ch]))

        if i in letter_pos and ch in subs_letter:
            opts = list(dict.fromkeys(opts + subs_letter[ch]))

        if i == 10 and ch not in ("H", "M"):
            opts = ["H", "M", ch]

        if i == 16:
            if ch in subs_digit:
                opts = list(dict.fromkeys(opts + subs_digit[ch]))
            if ch in subs_letter:
                opts = list(dict.fromkeys(opts + subs_letter[ch]))

        options.append(opts)

    out = []
    for combo in product(*options):
        out.append("".join(combo))
        if len(out) >= max_variants:
            break
    return out


def strip_anio_prefix(cand: str) -> str:
    for pref in ("AODEREGISTRO", "ANODEREGISTRO"):
        if cand.startswith(pref):
            return cand[len(pref):]
    return cand


def extract_curp_best_effort(t: str) -> str | None:
    # directo
    t2 = re.sub(r"[^A-Z0-9\s]", " ", normalize(t))
    m = CURP_RE.search(t2)
    if m:
        return m.group(1) + m.group(2)

    # después de AÑO
    cand = extract_after_label(t, LABEL_ANIO_REG, max_capture=220)
    # o después de CURP
    if not cand:
        cand = extract_after_label(t, LABEL_CURP_ONLY, max_capture=260)
    if not cand or len(cand) < 18:
        return None

    cand = strip_anio_prefix(cand)
    max_scan = min(len(cand) - 17, 80)
    for start in range(0, max_scan):
        base18 = cand[start:start + 18]
        for v in generate_curp_variants(base18, max_variants=1200):
            if CURP_RE.fullmatch(v):
                return v

    return cand[:18]


def extract_clave_elector_best_effort(t: str) -> str | None:
    cand = extract_after_label(t, LABEL_CLAVE_ELECTOR_ANY, max_capture=140)
    if not cand:
        return None

    if len(cand) >= 18:
        for start in range(0, min(len(cand) - 17, 50)):
            chunk = cand[start:start + 18]
            if CLAVE_ELECTOR_RE.fullmatch(chunk):
                return chunk
        return cand[:18]

    return cand[:22] if len(cand) >= 8 else None


# ---------- análisis principal ----------
def analyze_ine(text_raw: str) -> dict:
    t = normalize(text_raw)
    score = 0
    hits = []

    for k in KEYWORDS_STRONG:
        if k in t:
            score += 4
            hits.append(f"kw_strong:{k}")
    for k in KEYWORDS_MED:
        if k in t:
            score += 1
            hits.append(f"kw_med:{k}")

    curp = extract_curp_best_effort(text_raw)
    if curp:
        if CURP_RE.fullmatch(curp):
            score += 4
            hits.append(f"pattern:CURP:{curp}")
        else:
            hits.append(f"curp_candidate:{curp}")

    ce = extract_clave_elector_best_effort(text_raw)
    if ce:
        if CLAVE_ELECTOR_RE.fullmatch(ce):
            score += 3
            hits.append(f"pattern:CLAVE_ELECTOR:{ce}")
        else:
            hits.append(f"ce_candidate:{ce}")

    red = [rf for rf in RED_FLAGS if rf in t]
    if red:
        score -= 10
        hits.append("red_flags:" + ",".join(red))

    verdict = (
        "INE_MUY_PROBABLE" if score >= 8 else
        "INE_POSIBLE" if score >= 5 else
        "NO_PARECE_INE"
    )
    if red and verdict != "NO_PARECE_INE":
        verdict = "INE_DETECTADA_PERO_PRUEBA_O_FALSA"

    return {
        "verdict": verdict,
        "score": score,
        "hits": hits,
        "curp": curp,
        "clave_elector": ce,
    }


def validate_pdf_contains_ine(pdf_bytes: bytes) -> dict:
    embedded = extract_text_embedded(pdf_bytes)
    r1 = analyze_ine(embedded)

    if len(embedded.strip()) < 30 or r1["score"] < 5:
        try:
            ocr_text = ocr_first_pages_best(pdf_bytes, dpi_scale=4)
            r2 = analyze_ine(ocr_text)
            return {"method": "OCR", "result": r2}
        except Exception as e:
            r1["hits"].append(f"ocr_failed:{type(e).__name__}:{e}")
            return {"method": "embedded_text", "result": r1}

    return {"method": "embedded_text", "result": r1}


# ---------- fetch desde URL ----------
def fetch_pdf_from_url(url: str, timeout: int = 25) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/pdf,*/*",
    }
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    data = r.content
    if not data.startswith(b"%PDF"):
        sample = data[:100].decode("latin-1", errors="ignore")
        raise ValueError(f"No parece PDF. Inicio: {sample!r}")
    return data


# ---------- mapping a payload para API ----------
def build_api_payload(raw: dict) -> dict:
    """
    raw = output de validate_pdf_contains_ine(pdf_bytes)
    Devuelve algo amigable para frontend.
    """
    r = raw["result"]
    verdict = r["verdict"]
    score = r["score"]
    curp = r.get("curp")
    clave = r.get("clave_elector")
    hits = r.get("hits", [])

    # bandera de validez “operativa”
    if verdict == "INE_MUY_PROBABLE":
        is_valid = True
        code = "OK"
        message = "Se detectó una credencial para votar del INE válida."
    elif verdict == "INE_DETECTADA_PERO_PRUEBA_O_FALSA":
        is_valid = False
        code = "INE_PRUEBA"
        message = "El archivo parece una credencial de prueba o no válida (leyendas de muestra/demostración)."
    elif verdict == "INE_POSIBLE":
        is_valid = False
        code = "INE_DUDOSA"
        message = "Se detectan algunos elementos de INE, pero no suficientes para considerarla válida."
    else:
        is_valid = False
        code = "NO_INE"
        message = "No se detectó una credencial de elector válida en el archivo."

    return {
        "is_valid": is_valid,
        "code": code,
        "message": message,
        "verdict": verdict,
        "score": score,
        "curp": curp,
        "clave_elector": clave,
        "hits": hits,
    }


def validate_ine_url(url: str) -> dict:
    """
    Función que usará Django:
    recibe URL de PDF y regresa payload listo para JSON.
    """
    pdf = fetch_pdf_from_url(url)
    raw = validate_pdf_contains_ine(pdf)
    payload = build_api_payload(raw)
    payload["method"] = raw["method"]
    payload["source_url"] = url
    return payload
