# prestamos/models.py
from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from libros.models import Libro
from usuarios.models import Usuario

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name="prestamos")
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="prestamos")
    fecha_prestamo = models.DateField(default=timezone.localdate)
    fecha_devolucion = models.DateField(null=True, blank=True)
    dias_plazo = models.PositiveSmallIntegerField(default=7)
    tarifa_retraso = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("1.50"))
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        indexes = [
            models.Index(fields=["usuario", "fecha_prestamo"]),
            models.Index(fields=["libro", "fecha_prestamo"]),
        ]

    def __str__(self):
        estado = "abierto" if self.abierta else f"devuelto {self.fecha_devolucion}"
        return f"{self.libro.isbn} -> {self.usuario.numero} ({estado})"

    @property
    def abierta(self) -> bool:
        return self.fecha_devolucion is None

    @property
    def fecha_vencimiento(self) -> date:
        return self.fecha_prestamo + timedelta(days=self.dias_plazo)

    def calcular_multa(self, fecha_devolucion: date) -> Decimal:
        dias_usados = (fecha_devolucion - self.fecha_prestamo).days
        retraso = max(0, dias_usados - int(self.dias_plazo))
        return Decimal(retraso) * self.tarifa_retraso

    @transaction.atomic
    def confirmar_prestamo(self):
        # Límite de préstamos abiertos por usuario
        abiertos = Prestamo.objects.filter(usuario=self.usuario, fecha_devolucion__isnull=True).count()
        if abiertos >= self.usuario.max_prestamos:
            raise ValidationError("El usuario alcanzó su límite de préstamos.")
        # Disponibilidad
        self.libro.prestar()
        self.save()

    @transaction.atomic
    def devolver(self, fecha_devolucion: date | None = None) -> Decimal:
        if not self.abierta:
            raise ValidationError("El préstamo ya fue devuelto.")
        fecha_devolucion = fecha_devolucion or timezone.localdate()
        multa = self.calcular_multa(fecha_devolucion)
        self.fecha_devolucion = fecha_devolucion
        self.multa = multa
        self.save(update_fields=["fecha_devolucion", "multa"])
        self.libro.devolver()
        return multa

