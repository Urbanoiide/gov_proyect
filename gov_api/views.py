from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from gov_api.validaciones.ine_validator import validate_ine_url
from . import models
from .serializers import (
    ApoyoSerializer,
    CategoriaApoyoSerializer,
    DocumentoSerializer,
    DocumentoExpedienteSerializer,
    EspecialidadSerializer,
    EspecialidadEvaluadorSerializer,
    EstadoSerializer,
    EvaluacionExpedienteSerializer,
    EvaluadorSerializer,
    ExpedienteSerializer,
    GeneroSerializer,
    HistorialEstadoExpedienteSerializer,
    InstitucionSerializer,
    NotificacionSerializer,
    PalabraClaveSerializer,
    PeriodoSerializer,
    PrerrequisitoSerializer,
    TipoDocumentoSerializer,
)

class ApoyoViewSet(viewsets.ModelViewSet):
    """ViewSet de los programas cursos y tramites que ofrece la aplicacion
    """
    queryset = models.Apoyo.objects.all()
    serializer_class = ApoyoSerializer
    parser_classes = (MultiPartParser, FormParser)

class CategoriaApoyoViewSet(viewsets.ModelViewSet):
    """Viewset para las Keywords de los apoyos
    """
    queryset = models.CategoriaApoyo.objects.all()
    serializer_class = CategoriaApoyoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    """ViewSet para las caractieristicas de los documentos requeridos
    """
    queryset = models.Documento.objects.all()
    serializer_class = DocumentoSerializer

class DocumentoExpedienteViewSet(viewsets.ModelViewSet):
    """ViewSet para listar los documentos asociados a un expediente
    """
    queryset = models.DocumentoExpediente.objects.all()
    serializer_class = DocumentoExpedienteSerializer

    @action(detail=True, methods=["post"], url_path="validar-ine")
    def validar_ine(self, request, pk=None):
        """
        Valida la INE usando la URL almacenada en DocumentoExpediente.
        Retorna payload amigable para frontend:
        {
          is_valid, code, message, verdict, score, curp, clave_elector, hits, method, source_url
        }
        """
        doc_exp = self.get_object()

        # AJUSTA ESTE CAMPO según tu modelo:
        # - puede ser doc_exp.doc_archivo.url
        # - o doc_exp.doce_url
        # - o doc_exp.documento_url
        # etc.
        ine_url = None

        # Intentos comunes (para que no truene si cambia el nombre):
        for attr in ("url", "archivo", "file", "documento", "doc_archivo", "doce_archivo", "doce_url"):
            if hasattr(doc_exp, attr):
                val = getattr(doc_exp, attr)
                # si es FileField, puede tener .url
                if hasattr(val, "url"):
                    ine_url = val.url
                elif isinstance(val, str):
                    ine_url = val
                if ine_url:
                    break

        if not ine_url:
            return Response(
                {
                    "is_valid": False,
                    "code": "NO_URL",
                    "message": "El documento no tiene URL/archivo asociado para validar.",
                },
                status=status.HTTP_200_OK,
            )

        try:
            payload = validate_ine_url(ine_url)
            return Response(payload, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "is_valid": False,
                    "code": "ERROR_INE",
                    "message": f"Error al procesar la INE: {e}",
                },
                status=status.HTTP_200_OK,
            )

class EspecialidadViewSet(viewsets.ModelViewSet):
    """ViewSet para listar la especialidad de los evaluadores 
    """
    queryset = models.Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class EspecialidadEvaluadorViewSet(viewsets.ModelViewSet):
    """ViewSet para listar la relacion entre evaluador y especialidad
    """
    queryset = models.EspecialidadEvaluador.objects.all()
    serializer_class = EspecialidadEvaluadorSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    """ViewSet para ver el estado geografico de un expediente"""
    queryset = models.Estado.objects.all()
    serializer_class = EstadoSerializer

class EvaluacionExpedienteViewSet(viewsets.ModelViewSet):
    """ViewSet para listar los multiples evaluaciones de un expediente
    """
    queryset = models.EvaluacionExpediente.objects.all()
    serializer_class = EvaluacionExpedienteSerializer

class EvaluadorViewSet(viewsets.ModelViewSet):
    """ViewSet para listar los evaluadores registrados
    """
    queryset = models.Evaluador.objects.all()
    serializer_class = EvaluadorSerializer

class ExpedienteViewSet(viewsets.ModelViewSet):
    """ViewSet para ver los expedientes registrados
    """
    queryset = models.Expediente.objects.all()
    serializer_class = ExpedienteSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    """ViewSet para ver el genero de la persona del expediente
    """
    queryset = models.Genero.objects.all()
    serializer_class = GeneroSerializer

class HistorialEstadoExpedienteViewSet(viewsets.ModelViewSet):
    """ViewSet para ver las multiples solicitudes de un expediente
    """
    queryset = models.HistorialEstadoExpediente.objects.all()
    serializer_class = HistorialEstadoExpedienteSerializer

class InstitucionViewSet(viewsets.ModelViewSet):
    """ViewSet para ver la institucion a la que pertenece el evaluador
    """
    queryset = models.Institucion.objects.all()
    serializer_class = InstitucionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    """ViewSet para ver las notificaciones de los expedientes
    """
    queryset = models.Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class PalabraClaveViewSet(viewsets.ModelViewSet):
    """ViewSet para ver las palabras clave de los apoyos
    """
    queryset = models.PalabraClave.objects.all()
    serializer_class = PalabraClaveSerializer
class PeriodoViewSet(viewsets.ModelViewSet):
    """ViewSet para el periodo de los apoyos
    """
    queryset = models.Periodo.objects.all()
    serializer_class = PeriodoSerializer

class PrerrequisitoViewSet(viewsets.ModelViewSet):
    """ViewSet para ver el los prerrequisitos de los apoyos
    """
    queryset = models.Prerrequisito.objects.all()
    serializer_class = PrerrequisitoSerializer

class TipoDocumentoViewSet(viewsets.ModelViewSet):
    """ViewSet para los tipos de documentos de los expedientes
    """
    queryset = models.TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
