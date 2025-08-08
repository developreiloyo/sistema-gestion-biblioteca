from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre", "numero", "max_prestamos"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej. Ana Souza",
                "autocomplete": "name",
            }),
            "numero": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej. U001",
                "autocomplete": "off",
            }),
            "max_prestamos": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1, "max": 10,
            }),
        }
        help_texts = {
            "numero": "Identificador único del usuario.",
            "max_prestamos": "Cantidad máxima de préstamos simultáneos.",
        }

    def clean_max_prestamos(self):
        v = self.cleaned_data["max_prestamos"]
        if v <= 0:
            raise forms.ValidationError("Debe ser mayor que 0.")
        return v
