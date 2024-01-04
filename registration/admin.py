# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from vendedor.models import Vendedor
# # Register your models here.

# # # # definimos el formulario personalizado para vendedor en admin
# # # class VendedorInline(admin.StackedInline):
# # #     model = Vendedor
# # #     can_delete = False
# # #     verbose_name_plural = 'Vendedor'

# # # # extiende el modelo de usuario para incluir el modelo Vendedor
# # # class CustomUserAdmin(UserAdmin):
# # #     inlines = (VendedorInline, )

# # # # reemplaza el UserAdmin estándar con el personalizado
# # # admin.site.unregister(User)
# # # admin.site.register(User, CustomUserAdmin)
