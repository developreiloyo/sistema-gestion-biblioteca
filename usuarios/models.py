# usuarios/models.py
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    numero = models.CharField(max_length=20, unique=True, db_index=True)
    max_prestamos = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.nombre} #{self.numero}"
