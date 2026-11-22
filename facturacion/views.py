from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    CategoriaForm,
    ClienteForm,
    CompraForm,
    DetalleCompraFormSet,
    DetalleVentaFormSet,
    MarcaForm,
    ProductoForm,
    ProveedorForm,
    VentaForm,
)
from .mixins import UsuarioRegistroMixin
from .models import (
    Categoria,
    Cliente,
    Compra,
    Marca,
    Producto,
    Proveedor,
    Venta,
)


class InicioView(TemplateView):
    template_name = "home.html"


# =====================================================================
# MARCAS
# =====================================================================
class MarcaListView(ListView):
    model = Marca
    template_name = "facturacion/marca_list.html"
    context_object_name = "marcas"


class MarcaCreateView(UsuarioRegistroMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = "facturacion/marca_form.html"
    success_url = reverse_lazy("facturacion:marca_list")

    def form_valid(self, form):
        messages.success(self.request, "Marca creada correctamente.")
        return super().form_valid(form)


class MarcaUpdateView(UsuarioRegistroMixin, UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = "facturacion/marca_form.html"
    success_url = reverse_lazy("facturacion:marca_list")

    def form_valid(self, form):
        messages.success(self.request, "Marca actualizada correctamente.")
        return super().form_valid(form)


class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = "facturacion/marca_confirm_delete.html"
    success_url = reverse_lazy("facturacion:marca_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            nombre = str(self.object)
            self.object.delete()
            messages.success(request, f"Marca '{nombre}' eliminada.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar esta marca porque tiene productos asociados.",
            )
            return redirect("facturacion:marca_list")


# =====================================================================
# CATEGORÍAS
# =====================================================================
class CategoriaListView(ListView):
    model = Categoria
    template_name = "facturacion/categoria_list.html"
    context_object_name = "categorias"


class CategoriaCreateView(UsuarioRegistroMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "facturacion/categoria_form.html"
    success_url = reverse_lazy("facturacion:categoria_list")

    def form_valid(self, form):
        messages.success(self.request, "Categoría creada correctamente.")
        return super().form_valid(form)


class CategoriaUpdateView(UsuarioRegistroMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "facturacion/categoria_form.html"
    success_url = reverse_lazy("facturacion:categoria_list")

    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada correctamente.")
        return super().form_valid(form)


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = "facturacion/categoria_confirm_delete.html"
    success_url = reverse_lazy("facturacion:categoria_list")

    def form_valid(self, form):
        messages.success(self.request, "Categoría eliminada correctamente.")
        return super().form_valid(form)


# =====================================================================
# PRODUCTOS
# =====================================================================
class ProductoListView(ListView):
    model = Producto
    template_name = "facturacion/producto_list.html"
    context_object_name = "productos"

    def get_queryset(self):
        qs = super().get_queryset().select_related("marca").prefetch_related("categorias")
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(marca__nombre__icontains=q))
        return qs


class ProductoDetailView(DetailView):
    model = Producto
    template_name = "facturacion/producto_detail.html"
    context_object_name = "producto"


class ProductoCreateView(UsuarioRegistroMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "facturacion/producto_form.html"
    success_url = reverse_lazy("facturacion:producto_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductoUpdateView(UsuarioRegistroMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "facturacion/producto_form.html"
    success_url = reverse_lazy("facturacion:producto_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "facturacion/producto_confirm_delete.html"
    success_url = reverse_lazy("facturacion:producto_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            nombre = str(self.object)
            self.object.delete()
            messages.success(request, f"Producto '{nombre}' eliminado.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar este producto porque está registrado en ventas o compras.",
            )
            return redirect("facturacion:producto_list")


# =====================================================================
# CLIENTES
# =====================================================================
class ClienteListView(ListView):
    model = Cliente
    template_name = "facturacion/cliente_list.html"
    context_object_name = "clientes"

    def get_queryset(self):
        qs = super().get_queryset()
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(cedula__icontains=q)
                | Q(nombres__icontains=q)
                | Q(apellidos__icontains=q)
            )
        return qs


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "facturacion/cliente_detail.html"
    context_object_name = "cliente"


class ClienteCreateView(UsuarioRegistroMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "facturacion/cliente_form.html"
    success_url = reverse_lazy("facturacion:cliente_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente registrado correctamente.")
        return super().form_valid(form)


class ClienteUpdateView(UsuarioRegistroMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "facturacion/cliente_form.html"
    success_url = reverse_lazy("facturacion:cliente_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "facturacion/cliente_confirm_delete.html"
    success_url = reverse_lazy("facturacion:cliente_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            nombre = str(self.object)
            self.object.delete()
            messages.success(request, f"Cliente '{nombre}' eliminado.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar este cliente porque tiene ventas registradas.",
            )
            return redirect("facturacion:cliente_list")


# =====================================================================
# PROVEEDORES
# =====================================================================
class ProveedorListView(ListView):
    model = Proveedor
    template_name = "facturacion/proveedor_list.html"
    context_object_name = "proveedores"


class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = "facturacion/proveedor_detail.html"
    context_object_name = "proveedor"


class ProveedorCreateView(UsuarioRegistroMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "facturacion/proveedor_form.html"
    success_url = reverse_lazy("facturacion:proveedor_list")

    def form_valid(self, form):
        messages.success(self.request, "Proveedor registrado correctamente.")
        return super().form_valid(form)


class ProveedorUpdateView(UsuarioRegistroMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "facturacion/proveedor_form.html"
    success_url = reverse_lazy("facturacion:proveedor_list")

    def form_valid(self, form):
        messages.success(self.request, "Proveedor actualizado correctamente.")
        return super().form_valid(form)


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = "facturacion/proveedor_confirm_delete.html"
    success_url = reverse_lazy("facturacion:proveedor_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            nombre = str(self.object)
            self.object.delete()
            messages.success(request, f"Proveedor '{nombre}' eliminado.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar este proveedor porque tiene compras registradas.",
            )
            return redirect("facturacion:proveedor_list")


# =====================================================================
# VENTAS (MAESTRO - DETALLE)
# =====================================================================
class VentaListView(ListView):
    model = Venta
    template_name = "facturacion/venta_list.html"
    context_object_name = "ventas"

    def get_queryset(self):
        return super().get_queryset().select_related("cliente")


class VentaDetailView(DetailView):
    model = Venta
    template_name = "facturacion/venta_detail.html"
    context_object_name = "venta"


class VentaDetallesMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["detalles_formset"] = DetalleVentaFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["detalles_formset"] = DetalleVentaFormSet(instance=self.object)
        return context

    def _guardar_venta_y_detalles(self, form, formset, es_edicion=False):
        with transaction.atomic():
            if es_edicion and self.object and self.object.pk:
                self.object.devolver_stock()

            self.object = form.save(commit=False)
            if self.request.user.is_authenticated and not self.object.user_id:
                self.object.user = self.request.user
            self.object.save()

            formset.instance = self.object
            detalles = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for detalle in detalles:
                if self.request.user.is_authenticated and not detalle.user_id:
                    detalle.user = self.request.user
                detalle.save()
            formset.save_m2m()

            self.object.calcular_totales()
            self.object.descontar_stock()

        messages.success(
            self.request,
            "Venta actualizada correctamente." if es_edicion else "Venta registrada correctamente.",
        )
        return redirect("facturacion:venta_detail", pk=self.object.pk)


class VentaCreateView(VentaDetallesMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = "facturacion/venta_form.html"

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["detalles_formset"]
        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, detalles_formset=formset))
        return self._guardar_venta_y_detalles(form, formset, es_edicion=False)


class VentaUpdateView(VentaDetallesMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = "facturacion/venta_form.html"

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["detalles_formset"]
        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, detalles_formset=formset))
        return self._guardar_venta_y_detalles(form, formset, es_edicion=True)


class VentaDeleteView(DeleteView):
    model = Venta
    template_name = "facturacion/venta_confirm_delete.html"
    success_url = reverse_lazy("facturacion:venta_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            self.object.devolver_stock()
            venta_id = self.object.pk
            self.object.delete()
        messages.success(request, f"Venta #{venta_id} eliminada y stock devuelto.")
        return redirect(self.success_url)


# =====================================================================
# COMPRAS (MAESTRO - DETALLE)
# =====================================================================
class CompraListView(ListView):
    model = Compra
    template_name = "facturacion/compra_list.html"
    context_object_name = "compras"

    def get_queryset(self):
        return super().get_queryset().select_related("proveedor")


class CompraDetailView(DetailView):
    model = Compra
    template_name = "facturacion/compra_detail.html"
    context_object_name = "compra"


class CompraDetallesMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["detalles_formset"] = DetalleCompraFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["detalles_formset"] = DetalleCompraFormSet(instance=self.object)
        return context

    def _guardar_compra_y_detalles(self, form, formset, es_edicion=False):
        with transaction.atomic():
            if es_edicion and self.object and self.object.pk:
                self.object.revertir_stock()

            self.object = form.save(commit=False)
            if self.request.user.is_authenticated and not self.object.user_id:
                self.object.user = self.request.user
            self.object.save()

            formset.instance = self.object
            detalles = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for detalle in detalles:
                if self.request.user.is_authenticated and not detalle.user_id:
                    detalle.user = self.request.user
                detalle.save()
            formset.save_m2m()

            self.object.calcular_totales()
            self.object.ingresar_stock()

        messages.success(
            self.request,
            "Compra actualizada correctamente." if es_edicion else "Compra registrada correctamente.",
        )
        return redirect("facturacion:compra_detail", pk=self.object.pk)


class CompraCreateView(CompraDetallesMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = "facturacion/compra_form.html"

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["detalles_formset"]
        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, detalles_formset=formset))
        return self._guardar_compra_y_detalles(form, formset, es_edicion=False)


class CompraUpdateView(CompraDetallesMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = "facturacion/compra_form.html"

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["detalles_formset"]
        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, detalles_formset=formset))
        return self._guardar_compra_y_detalles(form, formset, es_edicion=True)


class CompraDeleteView(DeleteView):
    model = Compra
    template_name = "facturacion/compra_confirm_delete.html"
    success_url = reverse_lazy("facturacion:compra_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            self.object.revertir_stock()
            compra_id = self.object.pk
            self.object.delete()
        messages.success(request, f"Compra #{compra_id} eliminada y stock revertido.")
        return redirect(self.success_url)