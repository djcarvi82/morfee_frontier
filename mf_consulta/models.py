from django.db import models

# Create your models here.

class Consulta(models.Model):
    nombre = models.CharField(max_length=20)
    coleccion = models.CharField(max_length=30)
    contenido = models.TextField(blank=True, null=True)
    clave = models.CharField(max_length=20)
    estado = models.CharField(max_length=10)
    cliente_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'consulta'
