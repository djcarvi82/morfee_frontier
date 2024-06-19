from django.db import models
from users.models import AuthCliente, UserMorfee

class ControlImportAse(models.Model):
    tipo = models.CharField(max_length=30)  # Liquidación | Retenciones | Pob. no asegurada
    periodo = models.CharField(max_length=6)    # YYYYMM | 202108
    recurso = models.FileField(upload_to='aseguramiento/%Y/%m/', null=True, blank=True)
    recurso_json = models.FileField(upload_to='aseguramiento/%Y/%m/', null=True, blank=True)
    estado = models.IntegerField()  # 1: Upload raw file | 2: 
    diccionario = models.CharField(max_length=500, null=True)
    cliente = models.ForeignKey(AuthCliente, models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(UserMorfee, models.SET_NULL, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'control_import_ase'

    def __str__(self):
        return self.tipo

    @property
    def created_str(self):
        return self.created_at.strftime("%Y-%m-%d")

