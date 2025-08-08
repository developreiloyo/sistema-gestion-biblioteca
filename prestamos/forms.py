# prestamos/forms.py (TEMPORAL)
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
        widgets = {"fecha_prestamo": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        cleaned = super().clean()
        libro: Libro = cleaned.get("libro")
        usuario: Usuario = cleaned.get("usuario")
        if not libro or not usuario:
            return cleaned
        if libro.ejemplares_disponibles <= 0:
            raise ValidationError("No hay ejemplares disponibles de este libro.")
        if Prestamo.objects.filter(libro=libro, usuario=usuario, fecha_devolucion__isnull=True).exists():
            raise ValidationError("Este usuario ya tiene un préstamo abierto de este libro.")
        return cleaned

class DevolucionForm(forms.Form):
    fecha_devolucion = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    def clean_fecha_devolucion(self):
        return self.cleaned_data.get("fecha_devolucion") or timezone.localdate()

