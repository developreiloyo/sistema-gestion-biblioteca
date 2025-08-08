from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "isbn", "ejemplares_totales", "ejemplares_disponibles"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "form-control"
            if getattr(field.widget, "input_type", "") in ("number",):
                css = "form-control"
            field.widget.attrs.update({"class": css})

