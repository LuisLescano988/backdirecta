from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Sector(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, default='Pendiente')
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategorias')
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return f"{self.padre.nombre + ' -> ' if self.padre else ''}{self.nombre}"

class Color(models.Model):
    nombre = models.CharField(max_length=100, default='Pendiente')
    descripcion = models.TextField(blank=True)
    descripcion_tecnica = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"

class Material(models.Model):
    nombre = models.CharField(max_length=100, default='Pendiente')
    descripcion = models.TextField()
    descripcion_tecnica = models.TextField(blank=True)
    gramaje = models.PositiveIntegerField(help_text="Peso en g/m²", null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.gramaje}g/m²)"
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

class TamanioPredefinido(models.Model):
    UNIDADES = [
        ('cm', 'Centímetros'),
        ('m', 'Metros')
    ]
    
    alto = models.DecimalField(max_digits=10, decimal_places=2)
    ancho = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=2, choices=UNIDADES)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.ancho}{self.unidad} x {self.alto}{self.unidad}"
    
    class Meta:
        verbose_name = "Tamaño Predefinido"
        verbose_name_plural = "Tamaños Predefinidos"

class Terminacion(models.Model):
    nombre = models.CharField(max_length=100, default='Pendiente')
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subtipos')
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.padre.nombre + ' -> ' if self.padre else ''}{self.nombre}"
    
    class Meta:
        verbose_name = "Terminación"
        verbose_name_plural = "Terminaciones"

class Producto(models.Model):
    TIPOS_COTIZADOR = [
        ('offset', 'Offset'),
        ('digital', 'Digital'),
        ('gran_formato', 'Gran Formato')
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    tipo_cotizador = models.CharField(max_length=20, choices=TIPOS_COTIZADOR)
    categorias = models.ManyToManyField(Categoria)
    usa_pliego = models.BooleanField(default=False, help_text="Indica si el producto trabaja con pliegos")
    oculto_tienda = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True,  default='2024-01-01 00:00:00')
    fecha_actualizacion = models.DateTimeField(auto_now=True,  default='2024-01-01 00:00:00')
    
    # Características del producto
    colores_disponibles = models.ManyToManyField(Color, through='ProductoColor')
    materiales_disponibles = models.ManyToManyField(Material, through='ProductoMaterial')
    tamanios_disponibles = models.ManyToManyField(TamanioPredefinido, through='ProductoTamanio')
    terminaciones_disponibles = models.ManyToManyField(Terminacion, through='ProductoTerminacion')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class ProductoColor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    precio_por_cm2 = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['producto', 'color']
        verbose_name = "Color del Producto"
        verbose_name_plural = "Colores del Producto"

class ProductoMaterial(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    precio_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['producto', 'material']
        verbose_name = "Material del Producto"
        verbose_name_plural = "Materiales del Producto"

class ProductoTamanio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tamanio = models.ForeignKey(TamanioPredefinido, on_delete=models.CASCADE)
    porcentaje_bonificacion = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['producto', 'tamanio']
        verbose_name = "Tamaño del Producto"
        verbose_name_plural = "Tamaños del Producto"

class ProductoTerminacion(models.Model):
    TIPOS_TERMINACION = [
        ('fija', 'Fija'),
        ('opcional', 'Opcional')
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.CASCADE)
    tipo_terminacion = models.CharField(max_length=10, choices=TIPOS_TERMINACION)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ['producto', 'terminacion']
        verbose_name = "Terminación del Producto"
        verbose_name_plural = "Terminaciones del Producto"

class TipoCliente(models.Model):
    nombre = models.CharField(max_length=100, default='Pendiente')
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Tipo de Cliente"
        verbose_name_plural = "Tipos de Cliente"

class MargenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, 
                                   validators=[MinValueValidator(-100), MaxValueValidator(100)])
    
    class Meta:
        unique_together = ['producto', 'tipo_cliente']
        verbose_name = "Margen del Producto"
        verbose_name_plural = "Márgenes del Producto"

class Oferta(models.Model):
    descripcion = models.TextField()
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    texto_boton = models.CharField(max_length=50)
    productos = models.ManyToManyField(Producto)
    destacada = models.BooleanField(default=False)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True,  default='2024-01-01 00:00:00')
    fecha_actualizacion = models.DateTimeField(auto_now=True,  default='2024-01-01 00:00:00')
    
    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"