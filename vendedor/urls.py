from django.urls import path
from .views import VendedorView, GenerarVenta1, RegistrarClienteView, GenerarVenta2, GenerarVenta3



urlpatterns = [
    path('', VendedorView.as_view(), name='vendedor'),
    path('generar_ventas1', GenerarVenta1.as_view(), name='ventas1'),
    path('registrar_cliente/', RegistrarClienteView.as_view(), name='registrar_cliente'),
    path('generar_ventas2', GenerarVenta2.as_view(), name='ventas2'),
    path('generar_ventas3', GenerarVenta3.as_view(), name='ventas3'),
]
