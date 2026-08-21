from django.http import HttpResponse
from django.urls import path

from .models import Categoria, Producto


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
    path('', inicio, name='inicio'),
]
