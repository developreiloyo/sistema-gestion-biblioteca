from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Libro
from .forms import LibroForm

class LibroListView(ListView):
    model = Libro
    paginate_by = 20
    ordering = ["titulo"]

class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    success_url = reverse_lazy("libros:list")
    def form_valid(self, form):
        messages.success(self.request, "Libro creado correctamente.")
        return super().form_valid(form)

class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    success_url = reverse_lazy("libros:list")
    def form_valid(self, form):
        messages.success(self.request, "Libro actualizado.")
        return super().form_valid(form)

class LibroDeleteView(DeleteView):
    model = Libro
    success_url = reverse_lazy("libros:list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Libro eliminado.")
        return super().delete(request, *args, **kwargs)

