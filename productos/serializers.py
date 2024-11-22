# productos/serializers.py
from rest_framework import serializers
from .models import (
    Producto, Sector, Categoria, Color, Material, 
    TamanioPredefinido, Terminacion, TipoCliente,
    ProductoColor, ProductoMaterial, ProductoTamanio, 
    ProductoTerminacion, MargenProducto, Oferta
)

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'padre', 'descripcion', 'activo', 'subcategorias']

    def get_subcategorias(self, obj):
        subcategorias = Categoria.objects.filter(padre=obj)
        return CategoriaSerializer(subcategorias, many=True).data

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'nombre', 'descripcion', 'descripcion_tecnica', 'activo']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'nombre', 'descripcion', 'descripcion_tecnica', 'gramaje', 'activo']

class TamanioPredefinidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TamanioPredefinido
        fields = ['id', 'alto', 'ancho', 'unidad', 'activo']

class TerminacionSerializer(serializers.ModelSerializer):
    subtipos = serializers.SerializerMethodField()

    class Meta:
        model = Terminacion
        fields = ['id', 'nombre', 'padre', 'descripcion', 'activo', 'subtipos']

    def get_subtipos(self, obj):
        subtipos = Terminacion.objects.filter(padre=obj)
        return TerminacionSerializer(subtipos, many=True).data

class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCliente
        fields = ['id', 'nombre', 'descripcion']

class ProductoColorSerializer(serializers.ModelSerializer):
    color_detail = ColorSerializer(source='color', read_only=True)

    class Meta:
        model = ProductoColor
        fields = ['color', 'precio_por_cm2', 'color_detail']

class ProductoMaterialSerializer(serializers.ModelSerializer):
    material_detail = MaterialSerializer(source='material', read_only=True)

    class Meta:
        model = ProductoMaterial
        fields = ['material', 'precio_minimo', 'material_detail']

class ProductoTamanioSerializer(serializers.ModelSerializer):
    tamanio_detail = TamanioPredefinidoSerializer(source='tamanio', read_only=True)

    class Meta:
        model = ProductoTamanio
        fields = ['tamanio', 'porcentaje_bonificacion', 'tamanio_detail']

class ProductoTerminacionSerializer(serializers.ModelSerializer):
    terminacion_detail = TerminacionSerializer(source='terminacion', read_only=True)

    class Meta:
        model = ProductoTerminacion
        fields = ['terminacion', 'tipo_terminacion', 'precio', 'terminacion_detail']

class MargenProductoSerializer(serializers.ModelSerializer):
    tipo_cliente_detail = TipoClienteSerializer(source='tipo_cliente', read_only=True)

    class Meta:
        model = MargenProducto
        fields = ['tipo_cliente', 'porcentaje', 'tipo_cliente_detail']

class ProductoSerializer(serializers.ModelSerializer):
    sector_detail = SectorSerializer(source='sector', read_only=True)
    categorias_detail = CategoriaSerializer(source='categorias', many=True, read_only=True)
    colores_disponibles = ProductoColorSerializer(many=True, source='productocolor_set')
    materiales_disponibles = ProductoMaterialSerializer(many=True, source='productomaterial_set')
    tamanios_disponibles = ProductoTamanioSerializer(many=True, source='productotamanio_set')
    terminaciones_disponibles = ProductoTerminacionSerializer(many=True, source='productoterminacion_set')
    margenes = MargenProductoSerializer(many=True, source='margenproducto_set')

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'imagen', 
            'sector', 'sector_detail',
            'tipo_cotizador', 'categorias', 'categorias_detail',
            'usa_pliego', 'oculto_tienda', 'destacado', 
            'precio_base', 'colores_disponibles', 
            'materiales_disponibles', 'tamanios_disponibles',
            'terminaciones_disponibles', 'margenes',
            'fecha_creacion', 'fecha_actualizacion'
        ]

    def create(self, validated_data):
        colores_data = validated_data.pop('productocolor_set', [])
        materiales_data = validated_data.pop('productomaterial_set', [])
        tamanios_data = validated_data.pop('productotamanio_set', [])
        terminaciones_data = validated_data.pop('productoterminacion_set', [])
        margenes_data = validated_data.pop('margenproducto_set', [])
        categorias_data = validated_data.pop('categorias', [])

        producto = Producto.objects.create(**validated_data)
        producto.categorias.set(categorias_data)

        for color_data in colores_data:
            ProductoColor.objects.create(producto=producto, **color_data)
        
        for material_data in materiales_data:
            ProductoMaterial.objects.create(producto=producto, **material_data)
        
        for tamanio_data in tamanios_data:
            ProductoTamanio.objects.create(producto=producto, **tamanio_data)
        
        for terminacion_data in terminaciones_data:
            ProductoTerminacion.objects.create(producto=producto, **terminacion_data)
        
        for margen_data in margenes_data:
            MargenProducto.objects.create(producto=producto, **margen_data)

        return producto

    def update(self, instance, validated_data):
        colores_data = validated_data.pop('productocolor_set', [])
        materiales_data = validated_data.pop('productomaterial_set', [])
        tamanios_data = validated_data.pop('productotamanio_set', [])
        terminaciones_data = validated_data.pop('productoterminacion_set', [])
        margenes_data = validated_data.pop('margenproducto_set', [])
        categorias_data = validated_data.pop('categorias', None)

        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categorias_data is not None:
            instance.categorias.set(categorias_data)

        # Actualizar relaciones
        self._update_related_set(instance, 'productocolor_set', colores_data)
        self._update_related_set(instance, 'productomaterial_set', materiales_data)
        self._update_related_set(instance, 'productotamanio_set', tamanios_data)
        self._update_related_set(instance, 'productoterminacion_set', terminaciones_data)
        self._update_related_set(instance, 'margenproducto_set', margenes_data)

        return instance

    def _update_related_set(self, instance, relation_name, data):
        if data is not None:
            # Eliminar registros existentes
            getattr(instance, relation_name).all().delete()
            # Crear nuevos registros
            for item in data:
                getattr(instance, relation_name).create(**item)

class OfertaSerializer(serializers.ModelSerializer):
    productos_detail = ProductoSerializer(source='productos', many=True, read_only=True)

    class Meta:
        model = Oferta
        fields = [
            'id', 'descripcion', 'porcentaje_descuento',
            'fecha_inicio', 'fecha_fin', 'texto_boton',
            'productos', 'productos_detail', 'destacada',
            'creado_por', 'fecha_creacion', 'fecha_actualizacion'
        ]