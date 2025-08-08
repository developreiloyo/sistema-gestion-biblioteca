# prestamos/admin.py
from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("libro", "usuario", "fecha_prestamo", "fecha_devolucion", "dias_plazo", "tarifa_retraso", "multa")
    list_filter = ("fecha_devolucion",)
    search_fields = ("libro__isbn", "usuario__numero")


