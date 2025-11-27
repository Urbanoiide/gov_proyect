# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Apoyo(models.Model):
    apo_id = models.AutoField(primary_key=True)
    apo_nombre = models.CharField(max_length=50)
    apo_descripcion = models.TextField()
    apo_capacidad = models.IntegerField()
    apo_foto = models.TextField(blank=True, null=True)
    apo_fk_categoria = models.ForeignKey('CategoriaApoyo', models.DO_NOTHING, db_column='apo_fk_categoria', blank=True, null=True)
    apo_fk_periodo = models.ForeignKey('Periodo', models.DO_NOTHING, db_column='apo_fk_periodo')
    apo_fk_documento = models.ForeignKey('Documento', models.DO_NOTHING, db_column='apo_fk_documento')

    class Meta:
        managed = False
        db_table = 'apoyo'
    def __str__(self):
        return self.apo_nombre


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CategoriaApoyo(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_nombre = models.CharField(max_length=50)
    cat_descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria_apoyo'
    def __str__(self):
        return self.cat_nombre 



class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documento(models.Model):
    doc_id = models.AutoField(primary_key=True, db_comment='Id')
    doc_nombre = models.CharField(max_length=255, db_comment='Nombre')
    doc_descripcion = models.TextField(db_comment='Descripcion')
    doc_fk_tipo_documento = models.ForeignKey('TipoDocumento', models.DO_NOTHING, db_column='doc_fk_tipo_documento', db_comment='Tipo documento')

    class Meta:
        managed = False
        db_table = 'documento'

    def __str__(self):
        return self.doc_nombre  


class DocumentoExpediente(models.Model):
    doex_id = models.AutoField(primary_key=True)
    doex_fk_expediente = models.ForeignKey('Expediente', models.DO_NOTHING, db_column='doex_fk_expediente')
    doex_fk_documento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='doex_fk_documento')

    class Meta:
        managed = False
        db_table = 'documento_expediente'


class Especialidad(models.Model):
    esp_id = models.AutoField(primary_key=True)
    esp_nombre = models.CharField(max_length=50)
    esp_descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'especialidad'
    def __str__(self):
        return self.esp_nombre



class EspecialidadEvaluador(models.Model):
    eseva_id = models.AutoField(primary_key=True)
    eseva_fk_especialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='eseva_fk_especialidad')
    eseva_fk_evaluador = models.ForeignKey('Evaluador', models.DO_NOTHING, db_column='eseva_fk_evaluador')

    class Meta:
        managed = False
        db_table = 'especialidad_evaluador'


class Estado(models.Model):
    est_id = models.AutoField(primary_key=True)
    est_clave = models.CharField(unique=True, max_length=30)
    est_descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'
    def __str__(self):
        return self.est_clave


class EvaluacionExpediente(models.Model):
    eva_id = models.AutoField(primary_key=True)
    eva_fk_expediente = models.ForeignKey('Expediente', models.DO_NOTHING, db_column='eva_fk_expediente')
    eva_fk_valuador = models.ForeignKey('Evaluador', models.DO_NOTHING, db_column='eva_fk_valuador')
    eva_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    eva_comentarios = models.TextField(blank=True, null=True)
    eva_fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'evaluacion_expediente'
    


class Evaluador(models.Model):
    val_id = models.AutoField(primary_key=True)
    var_nombre = models.CharField(max_length=50)
    var_paterno = models.CharField(max_length=50)
    var_materno = models.CharField(max_length=50)
    var_fk_institucion = models.ForeignKey('Institucion', models.DO_NOTHING, db_column='var_fk_institucion')

    class Meta:
        managed = False
        db_table = 'evaluador'
    def __str__(self):
        return self.var_nombre + ' ' + self.var_paterno + ' ' + self.var_materno


class Expediente(models.Model):
    exp_id = models.AutoField(primary_key=True, db_comment='Id')
    exp_folio = models.CharField(max_length=255)
    exp_curp = models.CharField(unique=True, max_length=18, db_comment='Curp')
    exp_nombre = models.CharField(max_length=50, db_comment='Nombre')
    exp_paterno = models.CharField(max_length=50, db_comment='Paterno')
    exp_materno = models.CharField(max_length=50, blank=True, null=True, db_comment='Materno')
    exp_fk_genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='exp_fk_genero', blank=True, null=True, db_comment='Id genero')
    exp_descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')
    exp_fk_apoyo = models.ForeignKey(Apoyo, models.DO_NOTHING, db_column='exp_fk_apoyo', db_comment='Id curso')
    exp_fk_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='exp_fk_estado', db_comment='Id estado')
    exp_porcentaje = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, db_comment='Porcentaje')
    exp_fecha_creacion = models.DateTimeField(auto_now_add=True, db_comment='Fecha de creacion')
    exp_inr_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expediente'
    def __str__(self):
        return self.exp_curp + ' - ' + self.exp_folio + ' - ' + self.exp_nombre + ' ' + self.exp_paterno


class Genero(models.Model):
    gen_id = models.AutoField(primary_key=True, db_comment='Id')
    gen_nombre = models.CharField(max_length=25, db_comment='Nombre')
    gen_simbolo = models.CharField(max_length=1, db_comment='Simbolo')

    class Meta:
        managed = False
        db_table = 'genero'
    def __str__(self):
        return self.gen_nombre


class HistorialEstadoExpediente(models.Model):
    his_id = models.AutoField(primary_key=True)
    his_comentario = models.TextField(blank=True, null=True)
    his_usuario = models.CharField(max_length=100, blank=True, null=True)
    his_fecha_cambio = models.DateTimeField(auto_now_add=True)
    his_fk_notificacion = models.ForeignKey('Notificacion', models.DO_NOTHING, db_column='his_fk_notificacion')

    class Meta:
        managed = False
        db_table = 'historial_estado_expediente'


class Institucion(models.Model):
    ins_id = models.AutoField(primary_key=True)
    ins_nombre = models.CharField(max_length=50)
    ins_descripcion = models.TextField()
    ins_siglas = models.CharField(max_length=20)
    ins_correo = models.CharField(max_length=100)
    ins_numero = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'institucion'
    
    def __str__(self):
        return self.ins_nombre


class Notificacion(models.Model):
    not_id = models.AutoField(primary_key=True)
    not_fk_expediente = models.ForeignKey(Expediente, models.DO_NOTHING, db_column='not_fk_expediente', blank=True, null=True)
    not_canal = models.CharField(max_length=20)
    not_destino = models.TextField()
    not_asunto = models.CharField(max_length=50, blank=True, null=True)
    not_cuerpo = models.TextField()
    not_estado_envio = models.CharField(max_length=20)
    not_fecha_programada = models.DateTimeField(blank=True, null=True)
    not_fecha_envio = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notificacion'


class Periodo(models.Model):
    per_id = models.AutoField(primary_key=True, db_comment='Id')
    per_fecha_incio = models.DateTimeField(db_comment='Fecha inicio')
    pre_fecha_fin = models.DateTimeField(db_comment='fecha fin')
    pre_nombre = models.CharField(max_length=25, db_comment='Nombre')

    class Meta:
        managed = False
        db_table = 'periodo'
    def __str__(self):
        return self.pre_nombre 


class Prerrequisito(models.Model):
    pre_id = models.AutoField(primary_key=True, db_comment='Id')
    pre_fk_apoyo = models.ForeignKey(Apoyo, models.DO_NOTHING, db_column='pre_fk_apoyo', db_comment='Id apoyo')

    class Meta:
        managed = False
        db_table = 'prerrequisito'


class TipoDocumento(models.Model):
    tid_id = models.AutoField(primary_key=True)
    tid_nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_documento'
    def __str__(self):
        return self.tid_nombre
