from unittest.util import _MAX_LENGTH
from bson.json_util import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class AuthCliente(models.Model):
    cliente = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    contacto = models.CharField(max_length=30)
    modulos = models.CharField(max_length=100, blank=True)
    is_indigena = models.BooleanField()

    class Meta:
        db_table = 'auth_cliente'

    @property
    def badges(self):
        return self.modulos.split("|")

    @property
    def sp(self):
        return 'Salud Pública'

    @property
    def modulos_to_dict(self):
        return dict.fromkeys(self.modulos.split("|"), True)

    def __str__(self):
        return self.cliente

class AuthModulo(models.Model):
    modulo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    clave = models.CharField(max_length=10)
    estado = models.CharField(max_length=20)

    class Meta:
        db_table = 'auth_modulo'

    def __str__(self):
        return self.modulo

class AuthRol(models.Model):
    rol = models.CharField(max_length=20)
    nivel = models.IntegerField()

    class Meta:
        db_table = 'auth_rol'

    def __str__(self):
        return self.rol

class UserMorfee(AbstractUser):
    cliente = models.ForeignKey(AuthCliente, models.SET_NULL, blank=True, null=True)
    rol = models.ForeignKey(AuthRol, models.SET_NULL, blank=True, null=True)

class Diccionario(models.Model):
    class DataOptions(models.TextChoices):
        MORFEE = 'Morfee'
        CLIENTE = 'Cliente'

    class TypeHeadOptions(models.TextChoices):
        AUTO = 'auto'
        FILE_PARSE = 'file_parse'
        FILE_FIXED = 'file_fixed'
        FILE_FREE = 'file_free'

    modulo = models.CharField(max_length=30)
    coleccion = models.CharField(max_length=50, unique=True)
    alias = models.CharField(max_length=50)
    campos = models.CharField(max_length=700)
    has_data = models.IntegerField(default=0)
    type_head = models.CharField(max_length=10, choices=TypeHeadOptions.choices, default=TypeHeadOptions.FILE_FREE)
    propietario = models.CharField(max_length=10, choices=DataOptions.choices, default=DataOptions.CLIENTE)
    cliente = models.ForeignKey(AuthCliente, models.SET_NULL, blank=True, null=True)
    reglas = models.CharField(max_length=200, blank=True, default='')
    tipo = models.CharField(max_length=10, default='final')

    class Meta:
        db_table = 'diccionario'

class ControlImportBasic(models.Model):
    campos = models.CharField(max_length=500, null=True)
    cliente = models.ForeignKey(AuthCliente, models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(UserMorfee, models.SET_NULL, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    coleccion = models.CharField(max_length=50, blank=True, default='')
    total = models.IntegerField(default=0)
    clave = models.CharField(max_length=20, null=True)
    estado = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'control_import_basic'

    @property
    def created_str(self):
        return self.created_at.strftime("%Y-%m-%d")
