from django.urls import path

from .views import (
    CategoriaCreateView,
    CategoriaDeleteView,
    CategoriaListView,
    CategoriaUpdateView,
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView,
    CompraCreateView,
    CompraDeleteView,
    CompraDetailView,
    CompraListView,
    CompraUpdateView,
    MarcaCreateView,
    MarcaDeleteView,
    MarcaListView,
    MarcaUpdateView,
    ProductoCreateView,
    ProductoDeleteView,
    ProductoDetailView,
    ProductoListView,
    ProductoUpdateView,
    ProveedorCreateView,
    ProveedorDeleteView,
    ProveedorDetailView,
    ProveedorListView,
    ProveedorUpdateView,
    VentaCreateView,
    VentaDeleteView,
    VentaDetailView,
    VentaListView,
    VentaUpdateView,
)

app_name = "facturacion"

urlpatterns = [
    # Marcas
    path("marcas/", MarcaListView.as_view(), name="marca_list"),
    path("marcas/nueva/", MarcaCreateView.as_view(), name="marca_create"),
    path("marcas/<int:pk>/editar/", MarcaUpdateView.as_view(), name="marca_update"),
    path("marcas/<int:pk>/eliminar/", MarcaDeleteView.as_view(), name="marca_delete"),
    # Categorías
    path("categorias/", CategoriaListView.as_view(), name="categoria_list"),
    path("categorias/nueva/", CategoriaCreateView.as_view(), name="categoria_create"),
    path("categorias/<int:pk>/editar/", CategoriaUpdateView.as_view(), name="categoria_update"),
    path("categorias/<int:pk>/eliminar/", CategoriaDeleteView.as_view(), name="categoria_delete"),
    # Productos
    path("productos/", ProductoListView.as_view(), name="producto_list"),
    path("productos/nuevo/", ProductoCreateView.as_view(), name="producto_create"),
    path("productos/<int:pk>/", ProductoDetailView.as_view(), name="producto_detail"),
    path("productos/<int:pk>/editar/", ProductoUpdateView.as_view(), name="producto_update"),
    path("productos/<int:pk>/eliminar/", ProductoDeleteView.as_view(), name="producto_delete"),
    # Clientes
    path("clientes/", ClienteListView.as_view(), name="cliente_list"),
    path("clientes/nuevo/", ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/", ClienteDetailView.as_view(), name="cliente_detail"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente_update"),
    path("clientes/<int:pk>/eliminar/", ClienteDeleteView.as_view(), name="cliente_delete"),
    # Proveedores
    path("proveedores/", ProveedorListView.as_view(), name="proveedor_list"),
    path("proveedores/nuevo/", ProveedorCreateView.as_view(), name="proveedor_create"),
    path("proveedores/<int:pk>/", ProveedorDetailView.as_view(), name="proveedor_detail"),
    path("proveedores/<int:pk>/editar/", ProveedorUpdateView.as_view(), name="proveedor_update"),
    path("proveedores/<int:pk>/eliminar/", ProveedorDeleteView.as_view(), name="proveedor_delete"),
    # Ventas
    path("ventas/", VentaListView.as_view(), name="venta_list"),
    path("ventas/nueva/", VentaCreateView.as_view(), name="venta_create"),
    path("ventas/<int:pk>/", VentaDetailView.as_view(), name="venta_detail"),
    path("ventas/<int:pk>/editar/", VentaUpdateView.as_view(), name="venta_update"),
    path("ventas/<int:pk>/eliminar/", VentaDeleteView.as_view(), name="venta_delete"),
    # Compras
    path("compras/", CompraListView.as_view(), name="compra_list"),
    path("compras/nueva/", CompraCreateView.as_view(), name="compra_create"),
    path("compras/<int:pk>/", CompraDetailView.as_view(), name="compra_detail"),
    path("compras/<int:pk>/editar/", CompraUpdateView.as_view(), name="compra_update"),
    path("compras/<int:pk>/eliminar/", CompraDeleteView.as_view(), name="compra_delete"),
]