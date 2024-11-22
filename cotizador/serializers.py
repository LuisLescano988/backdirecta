from rest_framework import serializers
from .models import (
    TipoClick, CargoPorBajada, Calidad, TipoImpresion,
    ConfiguracionCotizadorOffset, ConfiguracionCotizadorDigital,
    ConfiguracionCotizadorGranFormato, CantidadPersonalizada,
    IncrementoPorAdelanto, TipoPapel, CostoTerminacion
)
from productos.serializers import (
    MaterialSerializer, TamanioPredefinidoSerializer,
    TerminacionSerializer, ProductoSerializer
)

class CostoTerminacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostoTerminacion
        fields = '__all__'

class TipoClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoClick
        fields = '__all__'

class TipoPapelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPapel
        fields = '__all__'

class CargoPorBajadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoPorBajada
        fields = '__all__'

class CalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calidad
        fields = '__all__'

class TipoImpresionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoImpresion
        fields = '__all__'

class CantidadPersonalizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CantidadPersonalizada
        fields = ['cantidad', 'multiplicador']

class IncrementoPorAdelantoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncrementoPorAdelanto
        fields = ['dias', 'descripcion', 'porcentaje_incremento']

class ConfiguracionCotizadorOffsetSerializer(serializers.ModelSerializer):
    producto_detail = ProductoSerializer(source='producto', read_only=True)
    cantidades_personalizadas = CantidadPersonalizadaSerializer(many=True, source='cantidadpersonalizada_set')
    incrementos_adelanto = IncrementoPorAdelantoSerializer(many=True, source='incrementoporadelanto_set')

    class Meta:
        model = ConfiguracionCotizadorOffset
        fields = [
            'id', 'producto', 'producto_detail', 'mensaje_compra',
            'dias_produccion', 'tipo_medida', 'unidad_medida',
            'medida_minima', 'medida_maxima', 'dimensiones_fijas',
            'tipo_cantidad', 'cantidad_intervalo', 'cantidad_repeticiones',
            'cantidades_fijas', 'cantidades_personalizadas',
            'incrementos_adelanto', 'fecha_creacion', 'fecha_actualizacion'
        ]

    def create(self, validated_data):
        cantidades_data = validated_data.pop('cantidadpersonalizada_set', [])
        incrementos_data = validated_data.pop('incrementoporadelanto_set', [])
        
        config = ConfiguracionCotizadorOffset.objects.create(**validated_data)
        
        for cantidad in cantidades_data:
            CantidadPersonalizada.objects.create(configuracion=config, **cantidad)
        
        for incremento in incrementos_data:
            IncrementoPorAdelanto.objects.create(configuracion=config, **incremento)
        
        return config

    def update(self, instance, validated_data):
        cantidades_data = validated_data.pop('cantidadpersonalizada_set', [])
        incrementos_data = validated_data.pop('incrementoporadelanto_set', [])
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar cantidades personalizadas
        instance.cantidadpersonalizada_set.all().delete()
        for cantidad in cantidades_data:
            CantidadPersonalizada.objects.create(configuracion=instance, **cantidad)
        
        # Actualizar incrementos por adelanto
        instance.incrementoporadelanto_set.all().delete()
        for incremento in incrementos_data:
            IncrementoPorAdelanto.objects.create(configuracion=instance, **incremento)
        
        return instance

class ConfiguracionCotizadorDigitalSerializer(serializers.ModelSerializer):
    producto_detail = ProductoSerializer(source='producto', read_only=True)
    tipos_click_detail = TipoClickSerializer(source='tipos_click', many=True, read_only=True)
    tipos_papel_detail = MaterialSerializer(source='tipos_papel', many=True, read_only=True)
    medidas_detail = TamanioPredefinidoSerializer(source='medidas', many=True, read_only=True)
    tamanios_predefinidos_detail = TamanioPredefinidoSerializer(source='tamanios_predefinidos', many=True, read_only=True)
    terminaciones_fijas_detail = TerminacionSerializer(source='terminaciones_fijas', many=True, read_only=True)
    terminaciones_opcionales_detail = TerminacionSerializer(source='terminaciones_opcionales', many=True, read_only=True)

    class Meta:
        model = ConfiguracionCotizadorDigital
        fields = '__all__'

class ConfiguracionCotizadorGranFormatoSerializer(serializers.ModelSerializer):
    producto_detail = ProductoSerializer(source='producto', read_only=True)
    tipos_impresion_detail = TipoImpresionSerializer(source='tipos_impresion', many=True, read_only=True)
    calidades_detail = CalidadSerializer(source='calidades', many=True, read_only=True)
    materiales_detail = MaterialSerializer(source='materiales', many=True, read_only=True)
    terminaciones_fijas_detail = TerminacionSerializer