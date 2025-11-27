from django.conf import settings
from rest_framework import routers
from django.conf.urls.static import static
from django.urls import path, include
from .views import (
    ApoyoViewSet,
    CategoriaApoyoViewSet,
    DocumentoViewSet,
    DocumentoExpedienteViewSet,
    EspecialidadViewSet,
    EspecialidadEvaluadorViewSet,
    EstadoViewSet,
    EvaluacionExpedienteViewSet,
    EvaluadorViewSet,
    ExpedienteViewSet,
    GeneroViewSet,
    HistorialEstadoExpedienteViewSet,
    InstitucionViewSet,
    NotificacionViewSet,
    PeriodoViewSet,
    PrerrequisitoViewSet,
    TipoDocumentoViewSet,
)

router = routers.DefaultRouter()

router.register(r'apoyos', ApoyoViewSet)
router.register(r'categorias', CategoriaApoyoViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'documentos-expediente', DocumentoExpedienteViewSet)
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'especialidades-evaluador', EspecialidadEvaluadorViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'evaluacion-expediente', EvaluacionExpedienteViewSet)
router.register(r'evaluadores', EvaluadorViewSet)
router.register(r'expedientes', ExpedienteViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'historial-expediente', HistorialEstadoExpedienteViewSet)
router.register(r'instituciones', InstitucionViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'periodos', PeriodoViewSet)
router.register(r'prerrequisitos', PrerrequisitoViewSet)
router.register(r'tipos-documento', TipoDocumentoViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
