from django.urls import path
from .views import (
    LibroListView, LibroCreateView, LibroUpdateView, LibroDeleteView
)

app_name = "libros"

urlpatterns = [
    path("",       LibroListView.as_view(),   name="list"),
    path("nuevo/", LibroCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", LibroUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", LibroDeleteView.as_view(), name="delete"),
]
