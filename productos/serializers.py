from rest_framework import serializers
from .models import Producto, Sector, Cotizador, Categoria, Terminacion, Color, RangoCantidad

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'nombre', 'descripcion']

class CotizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizador
        fields = ['id', 'nombre', 'descripcion']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'categoria_padre']

class TerminacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminacion
        fields = ['id', 'nombre', 'monto']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'nombre', 'ganancia']

class RangoCantidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangoCantidad
        fields = ['id', 'rango_inicio', 'rango_fin', 'precio']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_base', 'descripcion', 'sectores', 'cotizadores', 
                  'categorias', 'terminaciones', 'colores', 'rangos_cantidad']
