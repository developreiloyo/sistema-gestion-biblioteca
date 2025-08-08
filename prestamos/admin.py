# prestamos/admin.py
from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "usuario", "libro", "fecha_prestamo", "fecha_devolucion",
        "get_dias_plazo", "get_tarifa_retraso", "get_multa",
    )
    search_fields = ("usuario__nombre", "libro__titulo", "libro__isbn")
    list_filter = ("fecha_devolucion",)

    def get_dias_plazo(self, obj):
        return getattr(obj, "dias_plazo", "")
    get_dias_plazo.short_description = "Días plazo"

    def get_tarifa_retraso(self, obj):
        return getattr(obj, "tarifa_retraso", "")
    get_tarifa_retraso.short_description = "Tarifa retraso"

    def get_multa(self, obj):
        # por si aún no hay lógica de multa
        try:
            return obj.multa
        except Exception:
            return ""
    get_multa.short_description = "Multa"


