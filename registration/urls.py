from django.urls import path
from .views import VendedorCreateView, SignUpView


urlpatterns = [
    path('crear_vendedor/', VendedorCreateView.as_view(), name='crear_vendedor'),
    path('signup/', SignUpView.as_view(), name='signup'),
]