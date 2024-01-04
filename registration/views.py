from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View
from django.urls import reverse_lazy
from vendedor.models import Vendedor
from vendedor.forms import VendedorForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django import forms



#aqui estamos manejando el inicio de sesion y como 
# son direccionados los dos tipos de usuarios + un mensaje de error en caso de
# que el usuario no sea ni vendedor ni jefe

class CustomLoginView(LoginView):
    # loque hará despues de ser validadocorrectamente el formulario
    def form_valid(self, form):
        #obtenemos la respuesta predeterinada de la validación del formilario
        response = super().form_valid(form)
        # Lógica de redirección basada en grupos
        return grupo_usuario(self.request)

# esta funcion nos ayuda a identificar el grupo al 
# cual pertenece el usuario y hacia donde redirigirlo  
def grupo_usuario(request):
    if request.user.groups.filter(name='jefeVentas').exists():
        # Usuario pertenece al grupo 'jefedeventas'
        return redirect('pagina_principal')
    elif request.user.groups.filter(name='vendedores').exists():
        # Usuario pertenece al grupo 'vendedor'
        return redirect('vendedor')
    else:
        # Usuario no pertenece a ninguno de los grupos, manejar según tus necesidades
        return render(request, 'registration/nuevo_perfil.html')
    
# incorporamos logout personalizado para 
# volver a la vista de login cuando hacemos logout   
class CustomLogoutView(LogoutView):
    # sobreescribe dispatchpara agregar lo que ocurre antes y despues de logout
    def dispatch(self, request, *args, **kwargs):
        # de la clase padre se obtiene la respuesta predeterminada del cierre de sesion 
        response = super().dispatch(request, *args, **kwargs)
        # redirecciona a la ruta vacia
        return redirect('/')
# crear instancias de la clase vendedor
class VendedorCreateView(CreateView):
    model = Vendedor #especifica el modelo de la BD
    form_class = VendedorForm #especifica el formulario
    template_name = 'jefeVentas/vendedores/formulario.html' # la template donde se utilizara
    success_url = reverse_lazy('pagina_principal')  # redirección tras la creación exitosa
    # cuando el formulario se valida de forma correcta
    def form_valid(self, form):
        # se agrega al grupo de vendedores
        form.instance.user.groups.add(Group.objects.get(name='vendedores'))  # asigna el usuario al objeto Vendedor
        # finalmente retorna el formulario validado para que se guarden en la BD
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    # la plantilla donde sera renderizado
    template_name = 'registration/sign_up.html'
    # devuelve la url a la que redirige después de que se envíe el formulario
    def get_success_url(self):
        return reverse_lazy('login') # Redirección tras la creación exitosa
    # personaliza los widgets de los campos de usuario y contrasenya
    def get_form(self, form_class = None):
        form = super(SignUpView, self).get_form()
        
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        # devuelve el formulario ya renderizado
        return form        
    

        



