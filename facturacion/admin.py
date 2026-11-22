from django.contrib import admin

from .models import (
    Categoria,
    Cliente,
    Compra,
    DetalleCompra,
    DetalleVenta,
    Marca,
    Perfil,
    Producto,
    Proveedor,
    Venta,
)


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_creacion", "fecha_modificacion")

    def save_model(self, request, obj, form, change):
        if not obj.user_id and request.user.is_authenticated:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in instances:
            if hasattr(obj, "user_id") and not obj.user_id and request.user.is_authenticated:
                obj.user = request.user
            obj.save()
        formset.save_m2m()


@admin.register(Categoria)
class CategoriaAdmin(BaseAdmin):
    list_display = ("nombre", "activo", "user", "fecha_creacion")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Marca)
class MarcaAdmin(BaseAdmin):
    list_display = ("nombre", "pais_origen", "activo", "user")
    list_filter = ("activo", "pais_origen")
    search_fields = ("nombre", "pais_origen")


@admin.register(Producto)
class ProductoAdmin(BaseAdmin):
    list_display = ("nombre", "marca", "precio", "stock", "activo")
    list_filter = ("activo", "marca", "categorias")
    search_fields = ("nombre", "descripcion")
    filter_horizontal = ("categorias",)


@admin.register(Cliente)
class ClienteAdmin(BaseAdmin):
    list_display = ("cedula", "apellidos", "nombres", "telefono", "email")
    search_fields = ("cedula", "apellidos", "nombres", "email")


@admin.register(Proveedor)
class ProveedorAdmin(BaseAdmin):
    list_display = ("ruc", "nombre", "apellido", "contacto", "email")
    search_fields = ("ruc", "nombre", "apellido", "email")


@admin.register(Perfil)
class PerfilAdmin(BaseAdmin):
    list_display = ("usuario", "cargo", "cedula", "telefono")
    search_fields = ("usuario__username", "cedula", "cargo")


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(BaseAdmin):
    list_display = ("id", "cliente", "tipo_pago", "subtotal", "iva", "total", "fecha_hora")
    list_filter = ("tipo_pago",)
    search_fields = ("cliente__cedula", "cliente__nombres", "cliente__apellidos")
    inlines = [DetalleVentaInline]


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1


@admin.register(Compra)
class CompraAdmin(BaseAdmin):
    list_display = ("id", "proveedor", "tipo_pago", "subtotal", "iva", "total", "fecha_hora")
    list_filter = ("tipo_pago",)
    search_fields = ("proveedor__ruc", "proveedor__nombre", "proveedor__apellido")
    inlines = [DetalleCompraInline]