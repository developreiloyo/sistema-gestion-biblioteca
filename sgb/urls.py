from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("libros/", include("libros.urls", namespace="libros")),
    path("usuarios/", include("usuarios.urls", namespace="usuarios")),
    path("prestamos/", include("prestamos.urls", namespace="prestamos")),
]
