from django.contrib import admin
from .models import Turno, Vendedor, Cliente, Venta, DetalleCompra, TipoDocumentoTributario, DocumentoTributario
# Register your models here.

class TurnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'hora_inicio', 'hora_termino', 'descripcion']  # Muestra los campos principales
    list_filter = ['nombre', 'hora_inicio', 'hora_termino']  # Permite filtrar por diferentes criterios
    search_fields = ['nombre', 'descripcion']  # Habilita la búsqueda por nombre y descripción

admin.site.register(Turno, TurnoAdmin)

class VendedorAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'run', 'fecha_nac', 'telefono', 'correo', 'turno', 'user']  # Campos a mostrar en la lista
    list_filter = ['turno']  # Filtro por turno
    search_fields = ['name', 'last_name', 'run', 'correo']  # Búsqueda por diferentes campos
    raw_id_fields = ['turno']  # Facilita la selección de turnos en la edición

admin.site.register(Vendedor, VendedorAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'apellido2', 'rut', 'telefono', 'direccion', 'giro', 'razon_social']  # Muestra los campos principales
    list_filter = ['giro', 'razon_social']  # Filtros por giro y razón social
    search_fields = ['nombre', 'apellido', 'apellido2', 'rut', 'razon_social']  # Búsqueda por diferentes criterios

admin.site.register(Cliente, ClienteAdmin)

class VentaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'subtotal', 'iva', 'precio_total', 'vendedor', 'cliente', 'caja']  # Campos a mostrar
    list_filter = ['fecha', 'vendedor', 'cliente', 'caja']  # Filtros para búsqueda
    search_fields = ['fecha', 'vendedor__name', 'vendedor__last_name', 'cliente__nombre']  # Búsqueda por diferentes criterios
    raw_id_fields = ['vendedor', 'cliente', 'caja']  # Facilita la selección de relaciones

admin.site.register(Venta, VentaAdmin)

class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'precio', 'venta']  # Campos a mostrar en la lista
    list_filter = ['producto', 'venta']  # Filtros para búsqueda
    search_fields = ['producto__nombre', 'venta__fecha']  # Búsqueda por nombre de producto o fecha de venta
    raw_id_fields = ['producto', 'venta']  # Facilita la selección de relaciones

admin.site.register(DetalleCompra, DetalleCompraAdmin)

class TipoDocumentoTributarioAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']  # Muestra el nombre del tipo de documento
    search_fields = ['nombre']  # Habilita la búsqueda por nombre

admin.site.register(TipoDocumentoTributario, TipoDocumentoTributarioAdmin)

class DocumentoTributarioAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'subtotal', 'iva', 'precio_total', 'tipo', 'vendedor', 'venta', 'cliente']  # Campos a mostrar
    list_filter = ['fecha', 'tipo', 'vendedor', 'venta', 'cliente']  # Filtros para búsqueda
    search_fields = ['fecha', 'tipo__nombre', 'vendedor__name', 'vendedor__last_name', 'venta__fecha', 'cliente__nombre']  # Búsqueda por diferentes criterios
    raw_id_fields = ['tipo', 'vendedor', 'venta', 'cliente']  # Facilita la selección de relaciones

admin.site.register(DocumentoTributario, DocumentoTributarioAdmin)