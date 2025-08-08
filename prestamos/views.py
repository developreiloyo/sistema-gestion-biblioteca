from datetime import date
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import PrestamoCreateForm, DevolucionForm
from .models import Prestamo
from usuarios.models import Usuario
from libros.models import Libro


class PrestamoListView(ListView):
    model = Prestamo
    paginate_by = 20
    ordering = ("-id",)


class PrestamoCreateView(CreateView):
    model = Prestamo
    form_class = PrestamoCreateForm
    template_name = "prestamos/prestamo_form.html"
    success_url = reverse_lazy("prestamos:list")

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Bloqueos a nivel de fila para evitar condiciones de carrera
                usuario = Usuario.objects.select_for_update().get(pk=form.cleaned_data["usuario"].pk)
                libro =   Libro.objects.select_for_update().get(pk=form.cleaned_data["libro"].pk)

                # Reglas de negocio (revalida aunque el form ya lo hizo)
                if libro.ejemplares_disponibles <= 0:
                    raise ValidationError("No hay ejemplares disponibles de este libro.")
                activos = Prestamo.objects.filter(usuario=usuario, fecha_devolucion__isnull=True).count()
                if activos >= getattr(usuario, "max_prestamos", 3):
                    raise ValidationError("El usuario alcanzó su máximo de préstamos activos.")

                # Crear préstamo
                self.object = form.save(commit=False)
                if not self.object.fecha_prestamo:
                    self.object.fecha_prestamo = timezone.localdate()
                self.object.save()

                # Descontar disponibilidad
                Libro.objects.filter(pk=libro.pk).update(
                    ejemplares_disponibles=F("ejemplares_disponibles") - 1
                )

            messages.success(self.request, "Préstamo registrado correctamente.")
            return redirect(self.get_success_url())

        except ValidationError as ve:
            form.add_error(None, ve.message)
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None, f"Ocurrió un error al crear el préstamo: {e}")
            return self.form_invalid(form)


class PrestamoDevolverView(View):
    template_name = "prestamos/devolver.html"   # ← usa tu template
    success_url = reverse_lazy("prestamos:list")

    def get(self, request, pk):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = DevolucionForm(initial={"fecha_devolucion": timezone.localdate()})
        return render(request, self.template_name, {"prestamo": prestamo, "form": form})

    def post(self, request, pk):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = DevolucionForm(request.POST or None)
        if not form.is_valid():
            messages.error(request, "Datos inválidos en la devolución.")
            return render(request, self.template_name, {"prestamo": prestamo, "form": form})

        fecha_dev = form.cleaned_data["fecha_devolucion"]
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update().get(pk=prestamo.libro_id)
                prestamo.fecha_devolucion = fecha_dev
                prestamo.clean()
                prestamo.save(update_fields=["fecha_devolucion"])
                Libro.objects.filter(pk=libro.pk).update(
                    ejemplares_disponibles=F("ejemplares_disponibles") + 1
                )
            messages.success(request, f"Devolución registrada. Multa: ${prestamo.multa}")
            return redirect(self.success_url)
        except ValidationError as ve:
            messages.error(request, ve.message)
        except Exception as e:
            messages.error(request, f"Ocurrió un error en la devolución: {e}")
        return render(request, self.template_name, {"prestamo": prestamo, "form": form})

    success_url = reverse_lazy("prestamos:list")

    def post(self, request, pk):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = DevolucionForm(request.POST or None)
        if not form.is_valid():
            messages.error(request, "Datos inválidos en la devolución.")
            return redirect(self.success_url)

        fecha_dev = form.cleaned_data["fecha_devolucion"]

        try:
            with transaction.atomic():
                # Bloquear libro; el préstamo ya lo tenemos
                libro = Libro.objects.select_for_update().get(pk=prestamo.libro_id)

                # Guardar devolución con validaciones del modelo
                prestamo.fecha_devolucion = fecha_dev
                prestamo.clean()  # puede lanzar ValidationError
                prestamo.save(update_fields=["fecha_devolucion"])

                # Devolver disponibilidad
                Libro.objects.filter(pk=libro.pk).update(
                    ejemplares_disponibles=F("ejemplares_disponibles") + 1
                )

            messages.success(request, f"Devolución registrada. Multa: ${prestamo.multa}")

        except ValidationError as ve:
            messages.error(request, ve.message)
        except Exception as e:
            messages.error(request, f"Ocurrió un error en la devolución: {e}")

        return redirect(self.success_url)

        



