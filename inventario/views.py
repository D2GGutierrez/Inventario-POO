from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Producto, Movimiento
from django.http import JsonResponse

class ProductoActivoMixin:

    def get_queryset(self):

        return (
            Producto.objects
            .select_related("categoria")
            .filter(activo=True)
        )

class ProductoListView(ProductoActivoMixin, ListView):

    model = Producto

    template_name = "inventario/producto_list.html"

    context_object_name = "productos"


class ProductoDetailView(ProductoActivoMixin, DetailView):

    model = Producto

    template_name = "inventario/producto_detail.html"

    context_object_name = "producto"


class ProductoCreateView(CreateView):

    model = Producto

    template_name = "inventario/producto_form.html"

    fields = [
        "sku",
        "nombre",
        "descripcion",
        "categoria",
        "proveedores",
        "precio",
        "stock",
        "stock_minimo",
        "activo",
    ]

    success_url = reverse_lazy("producto_list")


class ProductoUpdateView(UpdateView):

    model = Producto

    template_name = "inventario/producto_form.html"

    fields = [
        "sku",
        "nombre",
        "descripcion",
        "categoria",
        "proveedores",
        "precio",
        "stock",
        "stock_minimo",
        "activo",
    ]

    success_url = reverse_lazy("producto_list")


class MovimientoCreateView(CreateView):

    model = Movimiento

    template_name = "inventario/movimiento_form.html"

    fields = [
        "producto",
        "tipo",
        "cantidad",
        "nota",
    ]

    success_url = reverse_lazy("producto_list")


class MovimientoListView(ListView):

    model = Movimiento

    template_name = "inventario/movimiento_list.html"

    context_object_name = "movimientos"

    def get_queryset(self):

        return (
            Movimiento.objects
            .select_related("producto")
            .order_by("-creado")
        )




def api_productos(request):

    productos = Producto.objects.select_related(
        "categoria"
    ).filter(
        activo=True
    )

    data = []

    for producto in productos:

        data.append({

            "id": producto.id,

            "sku": producto.sku,

            "nombre": producto.nombre,

            "categoria": producto.categoria.nombre,

            "precio": float(producto.precio),

            "stock": producto.stock,

            "stock_minimo": producto.stock_minimo,

            "requiere_resurtido": producto.requiere_resurtido,

        })

    return JsonResponse(
        data,
        safe=False,
    )