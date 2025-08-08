from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Usuario
from .forms import UsuarioForm

class UsuarioListView(ListView):
    model = Usuario
    paginate_by = 20
    ordering = ["nombre"]

class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy("usuarios:list")
    def form_valid(self, form):
        messages.success(self.request, "Usuario creado.")
        return super().form_valid(form)

class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy("usuarios:list")
    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado.")
        return super().form_valid(form)

class UsuarioDeleteView(DeleteView):
    model = Usuario
    success_url = reverse_lazy("usuarios:list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado.")
        return super().delete(request, *args, **kwargs)

