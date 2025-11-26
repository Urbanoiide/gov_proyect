from rest_framework import serializers
from . import models

class ApoyoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source='apo_fk_categoria.cat_nombre', 
        read_only=True
    )
    periodo_nombre = serializers.CharField(
        source='apo_fk_periodo.pre_nombre', 
        read_only=True
    )
    documento_nombre = serializers.CharField(
        source='apo_fk_documento.doc_nombre',
        read_only=True
    )

    class Meta:
        model = models.Apoyo
        fields = [
            'apo_id',
            'apo_nombre',
            'apo_descripcion',
            'apo_capacidad',
            'apo_fk_categoria',
            'apo_fk_periodo',
            'apo_fk_documento',         
            'categoria_nombre',   
            'periodo_nombre', 
            'documento_nombre',
            ]          

class CategoriaApoyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoriaApoyo
        fields = '__all__'

        
class DocumentoSerializer(serializers.ModelSerializer):
    tipo_documento_nombre = serializers.CharField(
        source='doc_fk_tipo_documento.tid_nombre',
        read_only=True
    )
    class Meta:
        model = models.Documento
        fields = [
            'doc_id',
            'doc_nombre',
            'doc_descripcion',
            'tipo_documento_nombre',
        ]
class DocumentoExpedienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentoExpediente
        fields = '__all__'
class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Especialidad
        fields = '__all__'


class EspecialidadEvaluadorSerializer(serializers.ModelSerializer):
    especialidad_nombre = serializers.CharField(
        source='eseva_fk_especialidad.esp_nombre',
        read_only=True
    )
    evaluador_nombre = serializers.CharField(
        source='eseva_fk_evaluador.var_nombre',
        read_only=True
    )
    class Meta:
        model = models.EspecialidadEvaluador
        fields = '__all__'


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Estado
        fields = '__all__'
class EvaluacionExpedienteSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.EvaluacionExpediente
      fields = '__all__'
class EvaluadorSerializer(serializers.ModelSerializer):
    institucion_nombre = serializers.CharField(
        source='var_fk_institucion.ins_nombre',
        read_only=True
    )
    class Meta:
        model = models.Evaluador
        fields = [
                    'val_id',
                  'var_nombre',
                  'var_materno',
                  'var_paterno',
                  'institucion_nombre',
                  'var_fk_institucion',]
        
class ExpedienteSerializer(serializers.ModelSerializer):
    genero = serializers.CharField(
        source='exp_fk_genero.gen_nombre',
        read_only=True
    )
    apoyo = serializers.CharField(
        source='exp_fk_apoyo.apo_nombre',
        read_only=True
    )
    estado = serializers.CharField(
        source='exp_fk_estado.est_clave',
        read_only=True
    )
    class Meta:
        model = models.Expediente
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genero
        fields = '__all__'

class HistorialEstadoExpedienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistorialEstadoExpediente
        fields = '__all__'
class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institucion
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    folio = serializers.CharField(
        source='not_fk_expediente.exp_folio',  
        read_only=True
    )
    class Meta:
        model = models.Notificacion
        fields = '__all__'

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Periodo
        fields = '__all__'
class PrerrequisitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prerrequisito
        fields = '__all__'
class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoDocumento
        fields = '__all__'
    