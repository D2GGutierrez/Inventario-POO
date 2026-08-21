from django.contrib import admin

from .models import Categoria, Movimiento, Producto, Proveedor


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creado')
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre', 'correo')


class MovimientoInline(admin.TabularInline):
    model = Movimiento
    extra = 0
    readonly_fields = ('tipo', 'cantidad', 'nota', 'creado')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'nombre',
        'categoria',
        'precio',
        'stock',
        'stock_minimo',
        'requiere_resurtido',
        'activo',
    )
    list_filter = ('categoria', 'activo')
    search_fields = ('sku', 'nombre')
    inlines = [MovimientoInline]


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'nota', 'creado')
    list_filter = ('tipo',)
    search_fields = ('producto__sku', 'producto__nombre')
