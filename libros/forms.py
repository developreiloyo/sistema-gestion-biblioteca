from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "isbn", "ejemplares_totales", "ejemplares_disponibles"]
