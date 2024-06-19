from django.db import models

# Create your models here.
class Upload(models.Model):
    file = models.FileField(upload_to='pooja_files')
    class Meta:
        managed = False
