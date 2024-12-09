from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Sector(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Cotizador(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    categoria_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

class Terminacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, 
                                validators=[MinValueValidator(0), MaxValueValidator(10000000)])

    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    ganancia = models.DecimalField(max_digits=10, decimal_places=2, 
                                   validators=[MinValueValidator(-1000000), MaxValueValidator(10000000)])

    def __str__(self):
        return self.nombre

class RangoCantidad(models.Model):
    rango_inicio = models.PositiveIntegerField()
    rango_fin = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2, 
                                 validators=[MinValueValidator(-1000000), MaxValueValidator(100000000)])

    def __str__(self):
        return f"{self.rango_inicio} - {self.rango_fin}"

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    sectores = models.ManyToManyField(Sector)
    cotizadores = models.ManyToManyField(Cotizador)
    categorias = models.ManyToManyField(Categoria)
    terminaciones = models.ManyToManyField(Terminacion)
    colores = models.ManyToManyField(Color)
    rangos_cantidad = models.ManyToManyField(RangoCantidad)

    def __str__(self):
        return self.nombre
