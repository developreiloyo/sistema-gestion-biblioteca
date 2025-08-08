from django.db import models
from decimal import Decimal
from datetime import timedelta
from django.core.exceptions import ValidationError

class Prestamo(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    libro = models.ForeignKey('libros.Libro', on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)

    dias_plazo = models.PositiveSmallIntegerField(default=14)
    tarifa_retraso = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("2.50"))

    @property
    def multa(self):
        if not self.fecha_devolucion:
            return Decimal("0.00")
        venc = self.fecha_prestamo + timedelta(days=self.dias_plazo)
        retraso = (self.fecha_devolucion - venc).days
        if retraso <= 0:
            return Decimal("0.00")
        return (self.tarifa_retraso * Decimal(retraso)).quantize(Decimal("0.01"))

    def clean(self):
        if self.fecha_devolucion and self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError("La devolución no puede ser anterior al préstamo.")

