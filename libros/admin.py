# libros/admin.py
from django.contrib import admin
from .models import Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "isbn", "ejemplares_disponibles", "ejemplares_totales")
    search_fields = ("titulo", "autor", "isbn")

