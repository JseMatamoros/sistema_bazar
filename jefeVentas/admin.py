from django.contrib import admin
from vendedor.models import Categoria, Producto, Caja, Estado
# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']  # Muestra el nombre de la categoría
    list_filter = ['nombre']  # Permite filtrar por nombre
    search_fields = ['nombre']  # Habilita la búsqueda por nombre

admin.site.register(Categoria, CategoriaAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'sku', 'descripcion', 'stock', 'imagen', 'categoria']  # Campos del modelo Producto
    list_filter = ['categoria']
    search_fields = ['nombre', 'sku']  # Búsqueda por nombre y SKU
    readonly_fields = ['imagen']  # Imagen en modo solo lectura (opcional)

admin.site.register(Producto, ProductoAdmin)

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre']  # Solo el campo nombre

admin.site.register(Estado, EstadoAdmin)

class CajaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_creacion', 'jefeVentas', 'estado', 'fecha_termino']  # Usando los campos del modelo Caja
    list_filter = ['estado']
    search_fields = ['fecha_creacion']  # Opcional, ajusta el campo de búsqueda según tu preferencia

admin.site.register(Caja, CajaAdmin)
