# usuarios/admin.py
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "numero", "max_prestamos")
    search_fields = ("nombre", "numero")

