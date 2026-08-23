from django.http import HttpResponse
from django.urls import path

from .models import Categoria, Producto
from .views import (
    ProductoListView,
    ProductoDetailView,
    ProductoCreateView,
    ProductoUpdateView,
    MovimientoCreateView,
    MovimientoListView,
    api_productos,
)

def inicio(request):
    productos = Producto.objects.select_related('categoria').filter(activo=True)
    categorias = Categoria.objects.all()
    lineas = [
        '<h1>Inventario POO</h1>',
        f'<p>Categorías: {categorias.count()} | Productos activos: {productos.count()}</p>',
        '<ul>',
    ]
    for p in productos:
        alerta = ' (¡resurtir!)' if p.requiere_resurtido else ''
        lineas.append(f'<li>{p} — stock: {p.stock}{alerta}</li>')
    lineas.append('</ul>')
    return HttpResponse('\n'.join(lineas))


urlpatterns = [

    path("", inicio, name="inicio"),

    path(
        "productos/",
        ProductoListView.as_view(),
        name="producto_list",
    ),

    path(
        "productos/<int:pk>/",
        ProductoDetailView.as_view(),
        name="producto_detail",
    ),
    path(
        "productos/nuevo/",
        ProductoCreateView.as_view(),
        name="producto_create",
    ),
    path(
        "productos/<int:pk>/editar/",
        ProductoUpdateView.as_view(),
        name="producto_update",
    ),
    path(
        "movimientos/nuevo/",
        MovimientoCreateView.as_view(),
        name="movimiento_create",
    ),
    path(
        "movimientos/",
        MovimientoListView.as_view(),
        name="movimiento_list",
    ),
    path(
        "api/productos/",
        api_productos,
        name="api_productos",
    ),


]