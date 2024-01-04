from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from vendedor.models import Caja
from .views import Pagina_principal, Pagina_caja, CajaCreateView, CajaDetailView

class JefeVentasViewsTest(TestCase):
    def setUp(self):
        # Configurar un usuario de prueba con permisos de jefeVentas
        self.user = User.objects.create_user(username='jefe', password='testpassword')
        self.user.is_staff = True
        self.user.save()

    def test_pagina_principal_view(self):
        # Iniciar sesión con el usuario de prueba
        self.client.login(username='jefe', password='testpassword')
        response = self.client.get(reverse('pagina_principal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jefeVentas/home_jefeVentas.html')

    def test_pagina_caja_view(self):
        # Iniciar sesión con el usuario de prueba
        self.client.login(username='jefe', password='testpassword')
        response = self.client.get(reverse('pagina_caja'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jefeVentas/caja/caja.html')

    def test_caja_create_view(self):
        # Iniciar sesión con el usuario de prueba
        self.client.login(username='jefe', password='testpassword')
        response = self.client.get(reverse('caja_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jefeventas/caja/actualizar_caja.html')

    def test_caja_create_view_post(self):
        # Iniciar sesión con el usuario de prueba
        self.client.login(username='jefe', password='testpassword')

        # Simular una solicitud POST para crear una nueva caja
        data = {
            'campo1': 'valor1',
            # Incluye los demás campos necesarios
        }
        response = self.client.post(reverse('caja_create'), data)
        self.assertEqual(response.status_code, 200)  # O ajusta según el comportamiento esperado
        # Asegúrate de que la nueva caja se haya creado
        self.assertTrue(Caja.objects.filter(campo1='valor1').exists())

    def test_caja_detail_view(self):
        # Crear una caja de prueba
        caja = Caja.objects.create(campo1='valor1', jefeVentas=self.user.vendedor)

        # Iniciar sesión con el usuario de prueba
        self.client.login(username='jefe', password='testpassword')
        response = self.client.get(reverse('caja_detail', args=[caja.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jefeVentas/caja/detail.html')

    # Puedes agregar más pruebas para otras vistas y casos de borde
