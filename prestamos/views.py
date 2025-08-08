from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, View
from django.utils import timezone
from django.db import transaction
from libros.models import Libro
from usuarios.models import Usuario
from prestamos.models import Prestamo

from .models import Prestamo
from .forms import PrestamoCreateForm, DevolucionForm

class PrestamoListView(ListView):
    model = Prestamo
    paginate_by = 20

    def get_queryset(self):
        qs = Prestamo.objects.select_related("libro", "usuario").order_by("-fecha_prestamo")
        abiertos = self.request.GET.get("abiertos")
        if abiertos in {"1", "true", "True"}:
            qs = qs.filter(fecha_devolucion__isnull=True)
        return qs


class PrestamoCreateView(CreateView):
    model = Prestamo
    form_class = PrestamoCreateForm
    success_url = reverse_lazy("prestamos:list")

    @transaction.atomic
    def form_valid(self, form):
        try:
            # Creamos sin guardar (para llamar a confirmar_prestamo)
            obj: Prestamo = form.save(commit=False)
            obj.save()  # para tener PK si hace falta (no obligatorio)
            obj.confirmar_prestamo()
            messages.success(self.request, "Préstamo registrado correctamente.")
            return redirect(self.get_success_url())
        except ValidationError as e:
            # revertimos y devolvemos error en el form
            form.add_error(None, e.message if hasattr(e, "message") else e.messages)
            return self.form_invalid(form)


class PrestamoDevolverView(View):
    template_name = "prestamos/devolver.html"

    def get(self, request, pk):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        if not prestamo.fecha_devolucion:
            form = DevolucionForm(initial={"fecha_devolucion": timezone.localdate()})
        else:
            form = DevolucionForm()
            messages.info(request, "Este préstamo ya fue devuelto.")
        return render(request, self.template_name, {"prestamo": prestamo, "form": form})

    @transaction.atomic
    def post(self, request, pk):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = DevolucionForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"prestamo": prestamo, "form": form})
        try:
            fecha = form.cleaned_data.get("fecha_devolucion") or timezone.localdate()
            multa = prestamo.devolver(fecha)
            messages.success(request, f"Devolución registrada. Multa: R$ {multa:.2f}")
            return redirect(reverse("prestamos:list"))
        except ValidationError as e:
            form.add_error(None, e.message if hasattr(e, "message") else e.messages)
            return render(request, self.template_name, {"prestamo": prestamo, "form": form})
        



