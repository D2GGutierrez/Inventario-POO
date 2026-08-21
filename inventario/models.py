from django.core.validators import MinValueValidator
from django.db import models


class ModeloBase(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Categoria(ModeloBase):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(ModeloBase):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(ModeloBase):
    sku = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
    )
    proveedores = models.ManyToManyField(
        Proveedor,
        blank=True,
        related_name='productos',
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(
        default=0,
        help_text='Alerta cuando el stock sea menor o igual a este valor.',
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return f'{self.nombre} ({self.sku})'

    @property
    def requiere_resurtido(self) -> bool:
        return self.stock <= self.stock_minimo

    def ajustar_stock(self, cantidad: int) -> None:
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError('El stock no puede quedar en negativo.')
        self.stock = nuevo_stock
        self.save(update_fields=['stock', 'actualizado'])


class Movimiento(ModeloBase):
    class Tipo(models.TextChoices):
        ENTRADA = 'ENTRADA', 'Entrada'
        SALIDA = 'SALIDA', 'Salida'

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='movimientos',
    )
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    nota = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'{self.tipo} {self.cantidad} x {self.producto.nombre}'

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        super().save(*args, **kwargs)
        if es_nuevo:
            delta = self.cantidad if self.tipo == self.Tipo.ENTRADA else -self.cantidad
            self.producto.ajustar_stock(delta)
