from django.test import TestCase

from .models import Categoria, Movimiento, Producto, Proveedor


class ProductoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Uno')
        self.producto = Producto.objects.create(
            sku='SKU-001',
            nombre='Mouse',
            categoria=self.categoria,
            precio=199.99,
            stock=10,
            stock_minimo=3,
        )
        self.producto.proveedores.add(self.proveedor)

    def test_str_producto(self):
        self.assertEqual(str(self.producto), 'Mouse (SKU-001)')

    def test_ajustar_stock_entrada(self):
        self.producto.ajustar_stock(5)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)

    def test_ajustar_stock_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            self.producto.ajustar_stock(-11)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)

    def test_requiere_resurtido(self):
        self.assertFalse(self.producto.requiere_resurtido)
        self.producto.ajustar_stock(-7)
        self.assertTrue(self.producto.requiere_resurtido)


class MovimientoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Papelería')
        self.producto = Producto.objects.create(
            sku='SKU-002',
            nombre='Cuaderno',
            categoria=self.categoria,
            precio=45.00,
            stock=100,
            stock_minimo=10,
        )

    def test_entrada_aumenta_stock(self):
        Movimiento.objects.create(
            producto=self.producto,
            tipo=Movimiento.Tipo.ENTRADA,
            cantidad=20,
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 120)

    def test_salida_disminuye_stock(self):
        Movimiento.objects.create(
            producto=self.producto,
            tipo=Movimiento.Tipo.SALIDA,
            cantidad=30,
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 70)

    def test_salida_mayor_al_stock_no_deja_negativo(self):
        with self.assertRaises(ValueError):
            Movimiento.objects.create(
                producto=self.producto,
                tipo=Movimiento.Tipo.SALIDA,
                cantidad=101,
            )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 100)
