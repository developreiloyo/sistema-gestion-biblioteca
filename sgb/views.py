from django.shortcuts import render
from libros.models import Libro
from usuarios.models import Usuario
from prestamos.models import Prestamo

def home(request):
    ctx = {
        "libros_count": Libro.objects.count(),
        "usuarios_count": Usuario.objects.count(),
        "prestamos_count": Prestamo.objects.count(),
    }
    return render(request, "home.html", ctx)