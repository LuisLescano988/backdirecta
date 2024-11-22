from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    TipoClick, CargoPorBajada, Calidad, TipoImpresion,
    ConfiguracionCotizadorOffset, ConfiguracionCotizadorDigital,
    ConfiguracionCotizadorGranFormato, TipoPapel, CostoTerminacion
)
from .serializers import (
    TipoClickSerializer, CargoPorBajadaSerializer, CalidadSerializer,
    TipoImpresionSerializer, ConfiguracionCotizadorOffsetSerializer,
    ConfiguracionCotizadorDigitalSerializer, ConfiguracionCotizadorGranFormatoSerializer,
    TipoPapelSerializer, CostoTerminacionSerializer
)
from productos.models import Producto

class TipoClickViewSet(viewsets.ModelViewSet):
    queryset = TipoClick.objects.all()
    serializer_class = TipoClickSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TipoClick.objects.all()
        activo = self.request.query_params.get('activo', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset

class CargoPorBajadaViewSet(viewsets.ModelViewSet):
    queryset = CargoPorBajada.objects.all()
    serializer_class = CargoPorBajadaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CargoPorBajada.objects.all()
        activo = self.request.query_params.get('activo', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset.order_by('desde')

class CalidadViewSet(viewsets.ModelViewSet):
    queryset = Calidad.objects.all()
    serializer_class = CalidadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Calidad.objects.all()
        activo = self.request.query_params.get('activo', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset

class TipoImpresionViewSet(viewsets.ModelViewSet):
    queryset = TipoImpresion.objects.all()
    serializer_class = TipoImpresionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TipoImpresion.objects.all()
        activo = self.request.query_params.get('activo', None)
        moneda = self.request.query_params.get('moneda', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        if moneda:
            queryset = queryset.filter(moneda=moneda.upper())
        
        return queryset

class ConfiguracionCotizadorOffsetViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionCotizadorOffset.objects.all()
    serializer_class = ConfiguracionCotizadorOffsetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ConfiguracionCotizadorOffset.objects.all()
        producto_id = self.request.query_params.get('producto', None)
        
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def por_producto(self, request):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response(
                {'error': 'Se requiere el parámetro producto_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        configuracion = get_object_or_404(ConfiguracionCotizadorOffset, producto_id=producto_id)
        serializer = self.get_serializer(configuracion)
        return Response(serializer.data)

class ConfiguracionCotizadorDigitalViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionCotizadorDigital.objects.all()
    serializer_class = ConfiguracionCotizadorDigitalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ConfiguracionCotizadorDigital.objects.all()
        producto_id = self.request.query_params.get('producto', None)
        
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def por_producto(self, request):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response(
                {'error': 'Se requiere el parámetro producto_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        configuracion = get_object_or_404(ConfiguracionCotizadorDigital, producto_id=producto_id)
        serializer = self.get_serializer(configuracion)
        return Response(serializer.data)

class ConfiguracionCotizadorGranFormatoViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionCotizadorGranFormato.objects.all()
    serializer_class = ConfiguracionCotizadorGranFormatoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ConfiguracionCotizadorGranFormato.objects.all()
        producto_id = self.request.query_params.get('producto', None)
        
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def por_producto(self, request):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response(
                {'error': 'Se requiere el parámetro producto_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        configuracion = get_object_or_404(ConfiguracionCotizadorGranFormato, producto_id=producto_id)
        serializer = self.get_serializer(configuracion)
        return Response(serializer.data)

class TipoPapelViewSet(viewsets.ModelViewSet):
    queryset = TipoPapel.objects.all()
    serializer_class = TipoPapelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TipoPapel.objects.all()
        activo = self.request.query_params.get('activo', None)
        tipo_click = self.request.query_params.get('tipo_click', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        if tipo_click:
            queryset = queryset.filter(tipo_click_id=tipo_click)
        
        return queryset

class CostoTerminacionViewSet(viewsets.ModelViewSet):
    queryset = CostoTerminacion.objects.all()
    serializer_class = CostoTerminacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CostoTerminacion.objects.all()
        terminacion_id = self.request.query_params.get('terminacion', None)
        tipo_cargo = self.request.query_params.get('tipo_cargo', None)
        moneda = self.request.query_params.get('moneda', None)
        
        if terminacion_id:
            queryset = queryset.filter(terminacion_id=terminacion_id)
        if tipo_cargo:
            queryset = queryset.filter(tipo_cargo=tipo_cargo)
        if moneda:
            queryset = queryset.filter(moneda=moneda.upper())
        
        return queryset