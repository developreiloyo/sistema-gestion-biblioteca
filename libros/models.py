# libros/models.py
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, db_index=True)
    ejemplares_totales = models.PositiveIntegerField(default=1)
    ejemplares_disponibles = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(ejemplares_totales__gte=0), name="libro_totales_gte_0"),
            models.CheckConstraint(check=models.Q(ejemplares_disponibles__gte=0), name="libro_disp_gte_0"),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.isbn})"

    def disponible(self) -> bool:
        return self.ejemplares_disponibles > 0

    def prestar(self):
        if not self.disponible():
            raise ValidationError("No hay ejemplares disponibles para este libro.")
        self.ejemplares_disponibles -= 1
        self.save(update_fields=["ejemplares_disponibles"])

    def devolver(self):
        if self.ejemplares_disponibles >= self.ejemplares_totales:
            raise ValidationError("No se puede exceder el total de ejemplares.")
        self.ejemplares_disponibles += 1
        self.save(update_fields=["ejemplares_disponibles"])

    def agregar_ejemplares(self, cantidad: int):
        if cantidad <= 0:
            raise ValidationError("La cantidad a agregar debe ser > 0.")
        self.ejemplares_totales += cantidad
        self.ejemplares_disponibles += cantidad
        self.save(update_fields=["ejemplares_totales", "ejemplares_disponibles"])

