document.addEventListener('DOMContentLoaded', function () {
    // definir filasDetalle desde su clase .table-bordered tbody tr
    const filasDetalle = document.querySelectorAll('.table-bordered tbody tr');
    // definir subtotal, iva y total
    let subtotal = 0;
    let iva = 0;
    let total = 0;
    // recore filas y extraer cantidad y precio
    filasDetalle.forEach(function (fila) {
        const cantidadElement = fila.querySelector('.cantidad');
        const precioElement = fila.querySelector('.precio');
        // verificar si los elementos existen
        if (cantidadElement && precioElement) {
            const cantidad = parseInt(cantidadElement.textContent);
            const precio = parseFloat(precioElement.textContent.replace('$', ''));
            // vamos sumando al subtotal
            subtotal += cantidad * precio;
        } else {
            console.error('Error: Elemento con clase "cantidad" o "precio" no encontrado en la fila.');
        }
    });
    // calcula el IVA y el total
    iva = subtotal * 0.19; // tasa de IVA del 19%
    total = subtotal + iva;
    // actualiza el contenido de los elementos
    document.getElementById('subtotal').textContent = `Subtotal: $${subtotal.toFixed(2)}`;
    document.getElementById('iva').textContent = `IVA (19%): $${iva.toFixed(2)}`;
    document.getElementById('total').textContent = `Total: $${total.toFixed(2)}`;
});
