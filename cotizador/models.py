from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TipoClick(models.Model):
    descripcion = models.CharField(max_length=100)
    moneda = models.CharField(
        max_length=3, 
        choices=[('ARS', 'Peso Argentino'), ('USD', 'Dólar')]
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Click"
        verbose_name_plural = "Tipos de Click"
        
    def __str__(self):
        return f"{self.descripcion} - {self.moneda} {self.precio}"

class CargoPorBajada(models.Model):
    desde = models.PositiveIntegerField()
    hasta = models.PositiveIntegerField()
    porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(-100), MaxValueValidator(100)]
    )
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Cargo por Bajada"
        verbose_name_plural = "Cargos por Bajada"
        ordering = ['desde']
        
    def __str__(self):
        return f"{self.desde}-{self.hasta}: {self.porcentaje}%"

class Calidad(models.Model):
    descripcion = models.CharField(max_length=100)
    porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Porcentaje de recargo o descuento",
        validators=[MinValueValidator(-100), MaxValueValidator(100)]
    )
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Calidad"
        verbose_name_plural = "Calidades"
        
    def __str__(self):
        return f"{self.descripcion} ({self.porcentaje}%)"

class TipoImpresion(models.Model):
    descripcion = models.CharField(max_length=100)
    costo_cm2 = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(
        max_length=3, 
        choices=[('ARS', 'Peso Argentino'), ('USD', 'Dólar')]
    )
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Impresión"
        verbose_name_plural = "Tipos de Impresión"
        
    def __str__(self):
        return f"{self.descripcion} - {self.moneda} {self.costo_cm2}/cm²"

class ConfiguracionBase(models.Model):
    producto = models.OneToOneField('productos.Producto', on_delete=models.CASCADE)
    mensaje_compra = models.TextField(blank=True)
    dias_produccion = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ConfiguracionCotizadorOffset(ConfiguracionBase):
    TIPOS_MEDIDA = [
        ('sin_medida', 'Sin Medida'),
        ('libre', 'Libre'),
        ('fijas', 'Fijas'),
        ('rangos', 'Rangos')
    ]
    
    TIPOS_CANTIDAD = [
        ('sin_cantidad', 'Sin Cantidad'),
        ('libre', 'Libre'),
        ('multiplo', 'Múltiplo'),
        ('fijas', 'Fijas'),
        ('personalizadas', 'Cantidades Personalizadas')
    ]
    
    tipo_medida = models.CharField(max_length=20, choices=TIPOS_MEDIDA, default='sin_medida')
    unidad_medida = models.CharField(max_length=10, blank=True)
    medida_minima = models.PositiveIntegerField(null=True, blank=True)
    medida_maxima = models.PositiveIntegerField(null=True, blank=True)
    dimensiones_fijas = models.CharField(max_length=255, blank=True, help_text="Valores separados por comas")
    
    tipo_cantidad = models.CharField(max_length=20, choices=TIPOS_CANTIDAD, default='sin_cantidad')
    cantidad_intervalo = models.PositiveIntegerField(null=True, blank=True)
    cantidad_repeticiones = models.PositiveIntegerField(null=True, blank=True)
    cantidades_fijas = models.CharField(max_length=255, blank=True, help_text="Valores separados por comas")

    class Meta:
        verbose_name = "Configuración Cotizador Offset"
        verbose_name_plural = "Configuraciones Cotizador Offset"

class CantidadPersonalizada(models.Model):
    configuracion = models.ForeignKey(ConfiguracionCotizadorOffset, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    multiplicador = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        ordering = ['cantidad']

class IncrementoPorAdelanto(models.Model):
    configuracion = models.ForeignKey(ConfiguracionCotizadorOffset, on_delete=models.CASCADE)
    dias = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=100)
    porcentaje_incremento = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        ordering = ['dias']

class ConfiguracionCotizadorDigital(ConfiguracionBase):
    tipos_click = models.ManyToManyField(TipoClick)
    tipos_papel = models.ManyToManyField('productos.Material')
    medidas = models.ManyToManyField('productos.TamanioPredefinido')
    tamanios_predefinidos = models.ManyToManyField('productos.TamanioPredefinido', related_name='config_digital_tamanios')
    terminaciones_fijas = models.ManyToManyField('productos.Terminacion', related_name='config_digital_fijas')
    terminaciones_opcionales = models.ManyToManyField('productos.Terminacion', related_name='config_digital_opcionales')
    
    class Meta:
        verbose_name = "Configuración Cotizador Digital"
        verbose_name_plural = "Configuraciones Cotizador Digital"

class ConfiguracionCotizadorGranFormato(ConfiguracionBase):
    tipos_impresion = models.ManyToManyField(TipoImpresion)
    calidades = models.ManyToManyField(Calidad)
    materiales = models.ManyToManyField('productos.Material')
    terminaciones_fijas = models.ManyToManyField('productos.Terminacion', related_name='config_granformato_fijas')
    terminaciones_opcionales = models.ManyToManyField('productos.Terminacion', related_name='config_granformato_opcionales')
    
    class Meta:
        verbose_name = "Configuración Cotizador Gran Formato"
        verbose_name_plural = "Configuraciones Cotizador Gran Formato"

class TipoPapel(models.Model):
    nombre = models.CharField(max_length=100)
    alto = models.DecimalField(max_digits=10, decimal_places=2)
    ancho = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(
        max_length=3, 
        choices=[('ARS', 'Peso Argentino'), ('USD', 'Dólar')]
    )
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_click = models.ForeignKey(TipoClick, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Papel"
        verbose_name_plural = "Tipos de Papel"
        
    def __str__(self):
        return f"{self.nombre} ({self.ancho}x{self.alto})"

class CostoTerminacion(models.Model):
    TIPOS_CARGO = [
        ('unidad', 'Cargo por Unidad'),
        ('pliego', 'Cargo por Pliego'),
        ('cantidad', 'Cargo por Cantidad'),
        ('cm2', 'Cargo por cm²')
    ]
    
    terminacion = models.ForeignKey('productos.Terminacion', on_delete=models.CASCADE)
    cargo_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_cargo = models.CharField(max_length=20, choices=TIPOS_CARGO)
    moneda = models.CharField(
        max_length=3, 
        choices=[('ARS', 'Peso Argentino'), ('USD', 'Dólar')]
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Costo de Terminación"
        verbose_name_plural = "Costos de Terminación"