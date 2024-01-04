from django import forms
from vendedor.models import Producto, Caja, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','precio','sku','descripcion', 'stock','imagen','categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.Textarea(attrs={'class' : 'form-control'}),
            'stock' : forms.TextInput(attrs={'class' : 'form-control'}),
            'imagen' : forms.ClearableFileInput(attrs={'class' : 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()


class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['monto_inicial']
        widgets = {
            'monto_inicial': forms.NumberInput(attrs={'class':'form-control'}),
            #'fecha_termino': forms.TextInput(attrs={'class':'form-control'})
        }

class CajaUpdateForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = []  # Eliminar todos los campos para que no sean editables manualmente
        widgets = {
            'estado': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'fecha_termino': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }