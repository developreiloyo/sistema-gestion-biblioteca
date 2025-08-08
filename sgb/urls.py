from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("libros/", include("libros.urls", namespace="libros")),
    path("usuarios/", include("usuarios.urls", namespace="usuarios")),
    path("prestamos/", include("prestamos.urls", namespace="prestamos")),
]
