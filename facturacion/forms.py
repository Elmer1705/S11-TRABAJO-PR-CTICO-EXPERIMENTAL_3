from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import (
    Categoria,
    Cliente,
    Compra,
    DetalleCompra,
    DetalleVenta,
    Marca,
    Producto,
    Proveedor,
    Venta,
)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "imagen",
            "marca",
            "categorias",
            "activo",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "imagen": forms.ClearableFileInput(),
            "categorias": forms.SelectMultiple(attrs={"size": 4}),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre", "pais_origen", "activo"]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "activo"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 2}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos", "email", "telefono", "direccion"]

    def clean_cedula(self):
        cedula = (self.cleaned_data.get("cedula") or "").strip()
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos numéricos.")
        return cedula


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "apellido", "ruc", "email", "contacto", "logo"]
        widgets = {
            "logo": forms.ClearableFileInput(),
        }

    def clean_ruc(self):
        ruc = (self.cleaned_data.get("ruc") or "").strip()
        if not ruc.isdigit() or len(ruc) != 13 or not ruc.endswith("001"):
            raise forms.ValidationError("El RUC debe tener 13 dígitos numéricos y terminar en 001.")
        return ruc


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["cliente", "fecha_hora", "tipo_pago"]
        widgets = {
            "fecha_hora": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ["producto", "cantidad", "precio"]


class BaseDetalleVentaFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        validos = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            producto = form.cleaned_data.get("producto")
            cantidad = form.cleaned_data.get("cantidad") or 0
            if producto and cantidad > 0:
                validos += 1
                if cantidad > producto.stock:
                    raise forms.ValidationError(
                        f"Stock insuficiente para '{producto.nombre}' (disponible: {producto.stock}, solicitado: {cantidad})."
                    )
        if validos == 0:
            raise forms.ValidationError("Debe agregar al menos un detalle de venta válido.")


DetalleVentaFormSet = inlineformset_factory(
    Venta,
    DetalleVenta,
    form=DetalleVentaForm,
    formset=BaseDetalleVentaFormSet,
    extra=1,
    can_delete=True,
)


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["proveedor", "fecha_hora", "tipo_pago"]
        widgets = {
            "fecha_hora": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ["producto", "cantidad", "precio"]


class BaseDetalleCompraFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        validos = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            producto = form.cleaned_data.get("producto")
            cantidad = form.cleaned_data.get("cantidad") or 0
            if producto and cantidad > 0:
                validos += 1
        if validos == 0:
            raise forms.ValidationError("Debe agregar al menos un detalle de compra válido.")


DetalleCompraFormSet = inlineformset_factory(
    Compra,
    DetalleCompra,
    form=DetalleCompraForm,
    formset=BaseDetalleCompraFormSet,
    extra=1,
    can_delete=True,
)