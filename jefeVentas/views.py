from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import TemplateView,DetailView,ListView,CreateView,UpdateView,DeleteView
from vendedor.models import Producto, Caja, Estado, DocumentoTributario, TipoDocumentoTributario, Vendedor, Venta
from .forms import ProductoForm, CajaForm, CajaUpdateForm
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse
from datetime import datetime
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from django.views import View







# Create your views here.
@method_decorator(login_required, name='dispatch')
class Pagina_principal(PermissionRequiredMixin,TemplateView):
    template_name = "jefeVentas/home_jefeVentas.html"
    permission_required = "vendedor.permiso_jefeVentas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendedor_actual = self.request.user.vendedor  # Asegúrate de tener este atributo en tu usuario
        cajas = Caja.objects.filter(jefeVentas=vendedor_actual)
        caja_abierta = any(caja.estado.nombre == 'Abierto' for caja in cajas)
        context['cajas'] = cajas
        context['caja_abierta'] = caja_abierta
        return context
    
    

#Vista para el invetario.
@method_decorator(login_required, name='dispatch')
class Pagina_inventario(PermissionRequiredMixin,ListView):
    model = Producto
    template_name = "jefeVentas/inventario/inventario.html"
    context_object_name= 'productos'
    permission_required = "vendedor.permiso_jefeVentas"

#Vista para las cajas
@method_decorator(login_required, name='dispatch')
class Pagina_caja(PermissionRequiredMixin,ListView):
    model = Caja
    template_name = "jefeVentas/caja/caja.html"
    context_object_name= 'cajas'
    permission_required = "vendedor.permiso_jefeVentas"

#Vista para los informes de ventas diarios.
@method_decorator(login_required, name='dispatch')
class Pagina_informe_diario(PermissionRequiredMixin,ListView):
    model = Venta
    template_name = "jefeVentas/informeVentas/informe_ventas.html"
    context_object_name = 'ventas'
    permission_required = "vendedor.permiso_jefeVentas"
    def get_queryset(self):
        
        return DocumentoTributario.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        vendedor_id = self.request.GET.get('vendedor')
        tipo_documento_id = self.request.GET.get('tipo_documento')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if vendedor_id:
            queryset = queryset.filter(vendedor_id=vendedor_id)

        if tipo_documento_id:
            queryset = queryset.filter(documentotributario__tipo_id=tipo_documento_id)

        if fecha_inicio and fecha_fin:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            queryset = queryset.filter(fecha__range=(fecha_inicio, fecha_fin))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendedores'] = Vendedor.objects.all()
        context['tipos_documento'] = TipoDocumentoTributario.objects.all()

        # Verifica si algún parámetro de filtro está presente
        vendedor = self.request.GET.get('vendedor')
        tipo_documento = self.request.GET.get('tipo_documento')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        # Establecer 'filtro_aplicado' en True si alguno de los filtros no está vacío
        context['filtro_aplicado'] = bool(vendedor or tipo_documento or fecha_inicio or fecha_fin)

        return context
    
    

@method_decorator(login_required, name='dispatch')
class ProductoCreateView(PermissionRequiredMixin,CreateView):
    
    model= Producto
    form_class =ProductoForm
    template_name='jefeventas/inventario/formulario.html'
    success_url = reverse_lazy('pagina_inventario')
    permission_required = "vendedor.permiso_jefeVentas"

    def form_valid(self, form):
        producto = form.save(commit=False)
        producto.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, prepara la respuesta JSON.
            data = {
                'status': 'success',
                'message': 'El producto se ha creado con éxito.'
            }
            # Devuelve una respuesta JSON con el estado y el mensaje.
            return JsonResponse(data)
        else:
            # Si no es una solicitud AJAX, sigue el flujo normal de redirección.
            return super().form_valid(form)

    def form_invalid(self, form):
        # Este método se llama si el formulario enviado no es válido.
        
        # Comprueba si la petición es una solicitud AJAX.
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, prepara la respuesta JSON con los errores.
            data = {
                'status': 'error',
                'message': 'El formulario contiene errores.',
                'errors': form.errors.as_json()  # Convierte los errores del formulario a JSON.
            }
            # Devuelve una respuesta JSON con el estado de error y los mensajes correspondientes.
            return JsonResponse(data, status=400)
        else:
            # Si no es una solicitud AJAX, sigue el flujo normal de mostrar el formulario con errores.
            return super().form_invalid(form)
        

@method_decorator(login_required, name='dispatch')
class ProductoUpdateView(PermissionRequiredMixin,UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'jefeVentas/inventario/edit_form.html'
    success_url = reverse_lazy('pagina_inventario')
    permission_required = "vendedor.permiso_jefeVentas"


@method_decorator(login_required, name='dispatch')
class ProductoDeleteView(PermissionRequiredMixin,DeleteView):
    model = Producto
    template_name = 'jefeVentas/inventario/delete.html'
    success_url = reverse_lazy('pagina_inventario')
    permission_required = "vendedor.permiso_jefeVentas"


@method_decorator(login_required, name='dispatch')
class ProductoDetailView(PermissionRequiredMixin,DetailView):
    model = Producto
    template_name = 'jefeVentas/inventario/detail.html'
    context_object_name = 'productos'
    permission_required = "vendedor.permiso_jefeVentas"

#CRUD de caja.
@method_decorator(login_required, name='dispatch')
class CajaCreateView(PermissionRequiredMixin,CreateView):
    model= Caja
    form_class = CajaForm
    template_name='jefeventas/caja/actualizar_caja.html'
    success_url = reverse_lazy('pagina_caja')
    permission_required = "vendedor.permiso_jefeVentas"


    def form_valid(self, form):
        # Asignar el estado por defecto "Abierto" a la nueva caja
        estado_abierto = Estado.objects.get(nombre="Abierto")
        caja = form.save(commit=False)
        
        # Asignar el vendedor actual al campo jefeVentas
        vendedor_actual = self.request.user.vendedor  # Asegúrate de tener este atributo en tu usuario
        caja.jefeVentas = vendedor_actual
        
        caja.estado = estado_abierto
        caja.save()
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, prepara la respuesta JSON.
            data = {
                'status': 'success',
                'message': 'La caja se ha creado con éxito.'
            }
            # Devuelve una respuesta JSON con el estado y el mensaje.
            return JsonResponse(data)
        else:
            # Si no es una solicitud AJAX, sigue el flujo normal de redirección.
            return super().form_valid(form)

    def form_invalid(self, form):
        # Este método se llama si el formulario enviado no es válido.
        
        # Comprueba si la petición es una solicitud AJAX.
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, prepara la respuesta JSON con los errores.
            data = {
                'status': 'error',
                'message': 'El formulario contiene errores.',
                'errors': form.errors.as_json()  # Convierte los errores del formulario a JSON.
            }
            # Devuelve una respuesta JSON con el estado de error y los mensajes correspondientes.
            return JsonResponse(data, status=400)
        else:
            # Si no es una solicitud AJAX, sigue el flujo normal de mostrar el formulario con errores.
            return super().form_invalid(form)
        
    
@method_decorator(login_required, name='dispatch')
class CajaDetailView(PermissionRequiredMixin,DetailView):
    model = Caja
    template_name = 'jefeVentas/caja/detail.html'
    context_object_name = 'cajas'
    permission_required = "vendedor.permiso_jefeVentas"
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        
        caja = super(CajaDetailView, self).get_object(queryset)

        if caja.jefeVentas != self.request.user.vendedor:
            raise Http404("No tienes permiso para ver esta caja")
        return caja


@method_decorator(login_required, name='dispatch')
class CajaUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required = "vendedor.permiso_jefeVentas"
    model = Caja
    form_class = CajaUpdateForm
    template_name = 'jefeVentas/caja/actualizar_caja.html'
    success_url = reverse_lazy('pagina_caja')

    def form_valid(self, form):
        caja = form.save(commit=False)
        
        if caja.estado.nombre == "Abierto":
            caja.estado = Estado.objects.get(nombre='Cerrado')  # Obtener el estado 'Cerrado'
            caja.fecha_termino = timezone.now()  # Asignar la fecha y hora actual al cerrar la caja
        else :
            caja.estado = Estado.objects.get(nombre='Abierto')
            caja.fecha_termino = None
        caja.save()
        return super().form_valid(form)

class DocumentoPDFView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        documento = get_object_or_404(DocumentoTributario, pk=pk)

        if self.request.resolver_match.url_name == 'factura_pdf':
            template_path = 'jefeVentas/informeVentas/informe_ventas_pdf.html'
        elif self.request.resolver_match.url_name == 'boleta_pdf':
            template_path = 'jefeVentas/informeVentas/boleta_pdf.html'
        else:
            return HttpResponse('Acción no válida')

        context = {'documento': documento}
        return self.get_pdf_response(context, template_path, documento.id)

    def get_pdf_response(self, context, template_path, documento_id):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="documento_tributario_{documento_id}.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
