from rest_framework import viewsets
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
    PeriodoSerializer,
    PrerrequisitoSerializer,
    TipoDocumentoSerializer,
)

class ApoyoViewSet(viewsets.ModelViewSet):
    """ViewSet de los programas cursos y tramites que ofrece la aplicacion
    """
    queryset = models.Apoyo.objects.all()
    serializer_class = ApoyoSerializer

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
