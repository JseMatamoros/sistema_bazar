from django.test import TestCase
from .models import Turno, Cargo, Vendedor, Categoria, Producto, Estado, Caja, Cliente, Venta, DetalleCompra, TipoDocumentoTributario, DocumentoTributario, Secciones
from django.contrib.auth.models import User

class TurnoModelTest(TestCase):
    def test_str_representation(self):
        turno = Turno(nombre='Mañana', hora_inicio='08:00:00', hora_termino='12:00:00', descripcion='Turno de la mañana')
        self.assertEqual(str(turno), 'Mañana')

class VendedorModelTest(TestCase):
    def test_full_name_representation(self):
        vendedor = Vendedor(name='John', last_name='Doe', run='123456789', fecha_nac='1990-01-01', correo='john@example.com')
        self.assertEqual(str(vendedor), 'John Doe')

class ProductoModelTest(TestCase):
    def test_str_representation(self):
        categoria = Categoria.objects.create(nombre='Electrónicos')
        producto = Producto(nombre='Laptop', precio=1000, sku='ABC123', descripcion='Potente laptop', stock=10, categoria=categoria)
        self.assertEqual(str(producto), 'Laptop')


