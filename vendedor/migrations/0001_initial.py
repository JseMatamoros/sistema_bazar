# Generated by Django 4.2.7 on 2023-12-25 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_termino', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('apellido2', models.CharField(max_length=200)),
                ('rut', models.CharField(max_length=13)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('giro', models.CharField(blank=True, max_length=200, null=True)),
                ('razon_social', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Secciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('permiso_jefeVentas', 'Permisos necesarios para el Jefe de Ventas'), ('permiso_vendedores', 'Permisos necesarios para los Vendedores')),
            },
        ),
        migrations.CreateModel(
            name='TipoDocumentoTributario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('hora_inicio', models.TimeField()),
                ('hora_termino', models.TimeField()),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('run', models.CharField(max_length=13)),
                ('fecha_nac', models.DateField()),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('correo', models.EmailField(max_length=254)),
                ('turno', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendedor.turno')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto_pagado', models.IntegerField(blank=True, null=True)),
                ('vuelto', models.IntegerField(blank=True, null=True)),
                ('subtotal', models.IntegerField(blank=True, null=True)),
                ('iva', models.FloatField(blank=True, null=True)),
                ('precio_total', models.IntegerField(blank=True, null=True)),
                ('caja', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='vendedor.caja')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendedor.cliente')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.vendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('sku', models.CharField(default='null', max_length=10)),
                ('descripcion', models.TextField()),
                ('stock', models.IntegerField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='product_img')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoTributario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('subtotal', models.IntegerField()),
                ('iva', models.FloatField()),
                ('precio_total', models.IntegerField()),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendedor.cliente')),
                ('detalleCompra', models.ManyToManyField(to='vendedor.detallecompra')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.tipodocumentotributario')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.vendedor')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.venta')),
            ],
        ),
        migrations.AddField(
            model_name='detallecompra',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.producto'),
        ),
        migrations.AddField(
            model_name='detallecompra',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.venta'),
        ),
        migrations.AddField(
            model_name='caja',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.estado'),
        ),
        migrations.AddField(
            model_name='caja',
            name='jefeVentas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedor.vendedor'),
        ),
    ]
