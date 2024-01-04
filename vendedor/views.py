from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.views import View
from .models import Venta, DetalleCompra, Producto, DocumentoTributario, Caja, Cliente
from .forms import VentasForm, DetalleCompraForm, ClienteForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from django.contrib import messages

# muestra la pagina principal de un vendedor requiere autenticacion
@method_decorator(login_required, name='dispatch')
class VendedorView(PermissionRequiredMixin, View):
    template_name = 'vendedor/vendedor.html' # aqui se renderizara
    permission_required = "vendedor.permiso_vendedores" # para el permiso de vendedores
    
    def get(self, request, *args, **kwargs): # se ejecuta cuando se recibe solicitud get
        # obtener el vendedor actualmente logueado
        vendedor = request.user.vendedor
        # obtener todas las ventas asociadas al vendedor
        ventas_vendedor_caja = Venta.objects.filter(vendedor=vendedor)
        # pasa las ventas al contexto
        context = {
            'ventas_vendedor_caja': ventas_vendedor_caja,
        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class GenerarVenta1(PermissionRequiredMixin,CreateView):
    model = Venta
    form_class = VentasForm
    template_name = 'ventas/generar_venta1.html'
    success_url = '/ventas/generar_venta2'
    permission_required = "vendedor.permiso_vendedores"

    def form_valid(self, form):
        try:
            # Asignar el cliente seleccionado en el formulario
            cliente = form.cleaned_data['cliente']
            form.instance.cliente = cliente
            
            # Asignar el vendedor actualmente logueado
            form.instance.vendedor = self.request.user.vendedor
            
            # Obtener la caja abierta
            caja_abierta = Caja.objects.last()

            #Verificar si la caja_abierta tiene estado == "Abierto"
            if caja_abierta.estado.nombre != "Abierto" or caja_abierta.monto_inicial <= 0:
                messages.error(self.request, 'No hay cajas abiertas disponibles', extra_tags='danger')
                raise  Http404('No hay cajas abiertas disponibles')
            
            # Asignar la caja abierta a la venta
            form.instance.caja = caja_abierta
            form.instance.fecha = timezone.now().date()
            messages.success(self.request, 'Cliente Asociado Con Exito', extra_tags='success')
            return super().form_valid(form)
        
        except Http404 as e:
            # No hay cajas abiertas, redirigir a alguna vista o mostrar un mensaje de error
            messages.error(self.request, 'No hay cajas abiertas disponibles', extra_tags='danger')
            return redirect('vendedor')  
        
    def get_success_url(self):
        return reverse_lazy('ventas2')

class RegistrarClienteView(CreateView):
    
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente_form.html'
    success_url = reverse_lazy('ventas1')
    
    def form_valid(self, form):
        
        cliente = form.save(commit=False)
        cliente.save()
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, prepara la respuesta JSON.
            data = {
                'status': 'success',
                'message': 'El cliente se ha creado con éxito.'
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
class GenerarVenta2(PermissionRequiredMixin, FormView):
    permission_required = "vendedor.permiso_vendedores"
    template_name = 'ventas/generar_venta2.html'
    form_class = DetalleCompraForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        
        # Agregar la información del detalle de compra
        ultima_venta = Venta.objects.last()
        context['detalle_compra'] = DetalleCompra.objects.filter(venta=ultima_venta)
        
        return context

    def form_valid(self, form):
        try:
            producto_id = self.request.POST.get('producto')
            cantidad = form.cleaned_data['cantidad']
            producto = Producto.objects.get(pk=producto_id)

            # Obtener o crear una nueva Venta si no existe
            ultima_venta = Venta.objects.last()
            if not ultima_venta:
                ultima_venta = Venta.objects.create()

            # Crear una instancia de DetalleCompra
            if producto.stock < cantidad:
                raise ValueError('No hay suficiente stock')
                
            detalle_compra = DetalleCompra(producto=producto, cantidad=cantidad, precio=producto.precio, venta=ultima_venta)
            detalle_compra.save()

            # Almacenar el ID de la Venta en la sesión para su uso posterior
            self.request.session['venta_previa_id'] = ultima_venta.id

            messages.success(self.request, 'Detalle de compra agregado correctamente', extra_tags='success')
            # Redirigir a la vista para crear la venta final
            return redirect('ventas2')
        
        except ValueError as e:
            messages.error(self.request, str(e), extra_tags='danger')
            return HttpResponse(str(e))

# necesito crear la vista para generar la venta final

@method_decorator(login_required, name='dispatch')
class GenerarVenta3(PermissionRequiredMixin, View):
    permission_required = "vendedor.permiso_vendedores"

    def get(self, request, *args, **kwargs):
        ultima_venta = Venta.objects.last()
        detalles_compra = DetalleCompra.objects.filter(venta=ultima_venta)
        

        # Calcular el subtotal basado en todos los detalles de compra asociados a la venta
        subtotal = detalles_compra.aggregate(total=Sum('precio'))['total'] or Decimal(0)
        iva = subtotal * Decimal('0.19')  # Suponiendo un IVA del 19%
        total = subtotal + iva

        return render(request, 'ventas/generar_venta3.html', {
            'subtotal': subtotal,
            'iva': iva,
            'total': total,
        })

    def post(self, request, *args, **kwargs):
        try:
            tipo_documento_elegido = request.POST.get('tipo_documento')
            monto_pagado = request.POST.get('monto_pagado')

            ultima_venta = Venta.objects.last()
            detalles_compra = DetalleCompra.objects.filter(venta=ultima_venta)
            caja_abierta = Caja.objects.last()
            
            
            subtotal = sum(detalle.precio * detalle.cantidad for detalle in detalles_compra)
            iva = subtotal * Decimal('0.19')  # Suponiendo un IVA del 19%
            total = subtotal + iva

            if int(monto_pagado)  >= total:
                vuelto = int(monto_pagado) - total
                ultima_venta.vuelto = vuelto
            else:
                return HttpResponse('Monto pagado insuficiente')

            ultima_venta.monto_pagado = monto_pagado
            ultima_venta.subtotal = subtotal
            ultima_venta.iva = iva 
            ultima_venta.precio_total = total
            ultima_venta.save()

            caja_abierta.monto_final = caja_abierta.monto_inicial
            caja_abierta.monto_final = caja_abierta.monto_final + total
            caja_abierta.save()

            if tipo_documento_elegido == '4':
                # Crear el documento tributario para Boleta
                nuevo_documento_tributario = DocumentoTributario.objects.create(
                    venta=ultima_venta,
                    subtotal=subtotal,
                    iva=iva,
                    precio_total=total,
                    tipo_id=tipo_documento_elegido,
                    fecha=timezone.now().date(),
                    vendedor=ultima_venta.vendedor
                )

                nuevo_documento_tributario.detalleCompra.set(detalles_compra)
                messages.success(request, 'Venta realizada exitosamente', extra_tags='success')
                return redirect('vendedor')
            
            elif tipo_documento_elegido == '5':
                # Crear el documento tributario para Factura
                cliente = ultima_venta.cliente
                nuevo_documento_tributario = DocumentoTributario.objects.create(
                    venta=ultima_venta,
                    subtotal=subtotal,
                    iva=iva,
                    precio_total=total,
                    tipo_id=tipo_documento_elegido,
                    fecha=timezone.now().date(),
                    vendedor=ultima_venta.vendedor,
                    cliente=cliente
                )
                nuevo_documento_tributario.detalleCompra.set(detalles_compra)
                messages.success(request, 'Venta realizada exitosamente', extra_tags='success')
                return redirect('vendedor')
        
        except ValueError as e:
            messages.error(request, str(e), extra_tags='danger')
            return HttpResponse(str(e))
        
        except Exception as e:
            messages.error(request, 'Error interno del servidor', extra_tags='danger')
            return HttpResponse("Error interno del Servidor")
        
        except Http404 as e:
            messages.error(request, str(e), extra_tags='danger')
            return HttpResponseNotFound(str(e))

