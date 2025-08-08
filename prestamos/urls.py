from django.urls import path
from .views import PrestamoListView, PrestamoCreateView, PrestamoDevolverView

app_name = "prestamos"

urlpatterns = [
    path("",       PrestamoListView.as_view(),   name="list"),
    path("nuevo/", PrestamoCreateView.as_view(), name="create"),
    path("<int:pk>/devolver/", PrestamoDevolverView.as_view(), name="devolver"),
]
