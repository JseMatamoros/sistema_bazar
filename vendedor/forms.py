from django import forms
from .models import Vendedor, Venta, DetalleCompra, Cliente
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import Group, AbstractUser,User

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['user', 'name', 'last_name', 'run','fecha_nac', 'telefono', 'direccion', 'correo', 'turno']
        widgets = {          
            'user': forms.Select(attrs={'class': 'form-control', 'type': 'select'}), 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'run': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}), 
        }

# recordar que este forms esta siendo usado para dar la opcion de agregar al cliente a una venta
class VentasForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'class':'form-control'}),
            'cliente': forms.Select(attrs={'class':'form-control'}),
        }
        
# este form sera para mostrar las ventas asociadas a un vendedor

# class VentaForm(forms.ModelForm):
#     class Meta:
#         model = Venta
#         fields = ['cliente']
#         widgets = {
#             'fecha': forms.DateInput(attrs={'class': 'form-control'}),
#         }


# DetalleCompraFormSet = inlineformset_factory(
#     Venta, DetalleCompra, fields=('producto', 'cantidad'), extra=1
# )

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
# formulario clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pedro Ramiro', 'label': 'Nombre', 'icon': 'bi bi-person-gear'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Poblete', 'label': 'Apellido', 'icon': 'bi bi-person-gear'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alcantara', 'label': 'Apellido2', 'icon': 'bi bi-person-gear'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '18369166-2', 'label': 'Rut', 'icon': 'bi bi-person-gear'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '954575726', 'label': 'Teléfono', 'icon': 'bi bi-person-gear'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Santa María 2001', 'label': 'Dirección', 'icon': 'bi bi-person-gear'}),
            'giro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Analista Programador', 'label': 'Trabajo', 'icon': 'bi bi-person-gear'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Santa María 2001', 'label': 'Dirección', 'icon': 'bi bi-person-gear'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PepsiCo, Inc.', 'label': 'Razón social', 'icon': 'bi bi-person-gear'}),
        }
