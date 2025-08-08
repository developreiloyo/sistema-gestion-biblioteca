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

    # -----------------------------
    # Encapsulamiento (getters/setters)
    # -----------------------------
    @property
    def tarifa(self) -> Decimal:
        """Getter 'seguro' para la tarifa por día de retraso."""
        return self.tarifa_retraso

    @tarifa.setter
    def tarifa(self, value):
        """Setter con validación."""
        v = Decimal(value)
        if v <= 0:
            raise ValidationError("La tarifa debe ser positiva.")
        self.tarifa_retraso = v

    @property
    def plazo(self) -> int:
        """Getter 'seguro' para los días de plazo del préstamo."""
        return self.dias_plazo

    @plazo.setter
    def plazo(self, value: int):
        """Setter con validación de rango (puedes ajustar límites)."""
        try:
            v = int(value)
        except (TypeError, ValueError):
            raise ValidationError("El plazo debe ser un entero.")
        if not (1 <= v <= 60):
            raise ValidationError("El plazo debe estar entre 1 y 60 días.")
        self.dias_plazo = v

    # -----------------------------
    # Propiedad calculada (no persiste en BD)
    # -----------------------------
    @property
    def multa(self) -> Decimal:
        if not self.fecha_devolucion:
            return Decimal("0.00")
        venc = self.fecha_prestamo + timedelta(days=self.dias_plazo)
        retraso = (self.fecha_devolucion - venc).days
        if retraso <= 0:
            return Decimal("0.00")
        return (self.tarifa_retraso * Decimal(retraso)).quantize(Decimal("0.01"))

    # -----------------------------
    # Validaciones de dominio
    # -----------------------------
    def clean(self):
        # coherencia temporal
        if self.fecha_devolucion and self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError("La devolución no puede ser anterior al préstamo.")
        # refuerzo de encapsulamiento a nivel de modelo (por si se asigna directo)
        if self.tarifa_retraso is None or Decimal(self.tarifa_retraso) <= 0:
            raise ValidationError("La tarifa por retraso debe ser positiva.")
        if self.dias_plazo is None or int(self.dias_plazo) < 1:
            raise ValidationError("El plazo debe ser al menos 1 día.")


