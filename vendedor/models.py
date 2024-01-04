from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Turno(models.Model):
    nombre = models.CharField(max_length=200, blank=False, null= False)
    hora_inicio = models.TimeField(blank=False, null= False)
    hora_termino = models.TimeField(blank=False, null= False)
    descripcion = models.TextField(blank=False, null= False)

    def __str__(self) -> str:
        return self.nombre

class Cargo(models.Model):
    user = models.CharField(max_length=50, blank=False, null=False)

class Vendedor(models.Model):
    name = models.CharField(max_length=200,null=False, blank=False)
    last_name = models.CharField(max_length=200,null=False, blank=False)
    run = models.CharField(max_length=13,null=False, blank=False)
    fecha_nac = models.DateField(null=False, blank=False)
    telefono = models.CharField(max_length=15,null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    correo = models.EmailField(null=False, blank=False)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    
    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)
    sku = models.CharField(max_length=10, null=False, blank=False, default= 'null')
    descripcion = models.TextField(null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)
    imagen = models.ImageField(null=True, blank= True,upload_to='product_img')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre   


class Caja(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    jefeVentas = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_termino = models.DateTimeField(null=True, blank=True)
    monto_inicial = models.IntegerField(null=False, blank=False, default=0)
    monto_final = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'Caja {self.id}'


class Cliente(models.Model):
    nombre = models.CharField(max_length=200, null= False, blank=False)
    apellido = models.CharField(max_length=200, null= False, blank=False)
    apellido2= models.CharField(max_length=200, null= False, blank=False)
    rut = models.CharField(max_length=13 ,null=False, blank=False)
    telefono = models.CharField(max_length=15,null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    giro = models.CharField(max_length=200,null=True, blank=True)
    razon_social = models.CharField(max_length=200,null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.nombre} {self.apellido}'


class Venta(models.Model):
    fecha = models.DateField(null=False, blank=False)
    monto_pagado = models.IntegerField(null=True, blank=True)
    vuelto = models.IntegerField(null=True, blank=True)
    subtotal = models.IntegerField(null=True, blank=True)
    iva = models.FloatField(null=True, blank=True)
    precio_total = models.IntegerField(null=True, blank=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, default='1')

    def __str__(self) -> str:
        return f'Venta {self.id}'


class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

    def __str__(self):
        return f'Detalle {self.id}'


class TipoDocumentoTributario(models.Model):
    nombre = models.CharField(max_length=200, null= False, blank=False)
    
    def __str__(self) -> str:
        return self.nombre


class DocumentoTributario(models.Model):
    fecha = models.DateField(null=False, blank=False)
    subtotal = models.IntegerField(null=False, blank=False)
    iva = models.FloatField(null=False, blank=False)
    precio_total = models.IntegerField(null=False, blank=False)
    tipo = models.ForeignKey(TipoDocumentoTributario, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    detalleCompra = models.ManyToManyField(DetalleCompra)

    def __str__(self) -> str:
        return f'Documento Tributario {self.id}'


class Secciones(models.Model):
    class Meta:
        permissions = (
            ("permiso_jefeVentas", "Permisos necesarios para el Jefe de Ventas"),
            ("permiso_vendedores", "Permisos necesarios para los Vendedores")
        )