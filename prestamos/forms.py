from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Prestamo
from usuarios.models import Usuario
from libros.models import Libro

class PrestamoCreateForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ["libro", "usuario", "fecha_prestamo", "dias_plazo", "tarifa_retraso"]
        widgets = {
            "fecha_prestamo": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        libro: Libro = cleaned.get("libro")
        usuario: Usuario = cleaned.get("usuario")
        if not libro or not usuario:
            return cleaned
        # Evitar préstamo si no hay disponibilidad o supera límite (lo volveremos a validar al confirmar)
        if libro.ejemplares_disponibles <= 0:
            raise ValidationError("No hay ejemplares disponibles de este libro.")
        # Evitar duplicado abierto del mismo libro al mismo usuario (regla útil)
        existe_abierto = Prestamo.objects.filter(
            libro=libro, usuario=usuario, fecha_devolucion__isnull=True
        ).exists()
        if existe_abierto:
            raise ValidationError("Este usuario ya tiene un préstamo abierto de este libro.")
        return cleaned


class DevolucionForm(forms.Form):
    fecha_devolucion = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    def cleaned_fecha(self):
        # helper (opcional)
        fecha = self.cleaned_data.get("fecha_devolucion")
        return fecha or timezone.localdate()
