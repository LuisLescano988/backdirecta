# productos/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import (
    Producto, Sector, Categoria, Color, Material,
    TamanioPredefinido, Terminacion, TipoCliente, Oferta
)
from .serializers import (
    ProductoSerializer, SectorSerializer, CategoriaSerializer,
    ColorSerializer, MaterialSerializer, TamanioPredefinidoSerializer,
    TerminacionSerializer, TipoClienteSerializer, OfertaSerializer
)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Producto.objects.all()
        
        # Filtros
        sector = self.request.query_params.get('sector', None)
        categoria = self.request.query_params.get('categoria', None)
        oculto = self.request.query_params.get('oculto', None)
        destacado = self.request.query_params.get('destacado', None)
        tipo_cotizador = self.request.query_params.get('tipo_cotizador', None)
        busqueda = self.request.query_params.get('busqueda', None)
        
        if sector:
            queryset = queryset.filter(sector_id=sector)
        if categoria:
            queryset = queryset.filter(categorias__id=categoria)
        if oculto is not None:
            queryset = queryset.filter(oculto_tienda=oculto.lower() == 'true')
        if destacado is not None:
            queryset = queryset.filter(destacado=destacado.lower() == 'true')
        if tipo_cotizador:
            queryset = queryset.filter(tipo_cotizador=tipo_cotizador)
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripcion__icontains=busqueda)
            )
            
        return queryset.distinct()

    @action(detail=True, methods=['post'])
    def toggle_destacado(self, request, pk=None):
        producto = self.get_object()
        producto.destacado = not producto.destacado
        producto.save()
        return Response({'destacado': producto.destacado})

    @action(detail=True, methods=['post'])
    def toggle_oculto(self, request, pk=None):
        producto = self.get_object()
        producto.oculto_tienda = not producto.oculto_tienda
        producto.save()
        return Response({'oculto_tienda': producto.oculto_tienda})

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticated]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Categoria.objects.all()
        principales = self.request.query_params.get('principales', None)
        
        if principales:
            queryset = queryset.filter(padre__isnull=True)
            
        return queryset

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticated]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

class TamanioPredefinidoViewSet(viewsets.ModelViewSet):
    queryset = TamanioPredefinido.objects.all()
    serializer_class = TamanioPredefinidoSerializer
    permission_classes = [IsAuthenticated]

class TerminacionViewSet(viewsets.ModelViewSet):
    queryset = Terminacion.objects.all()
    serializer_class = TerminacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Terminacion.objects.all()
        principales = self.request.query_params.get('principales', None)
        
        if principales:
            queryset = queryset.filter(padre__isnull=True)
            
        return queryset

class TipoClienteViewSet(viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = TipoClienteSerializer
    permission_classes = [IsAuthenticated]

class OfertaViewSet(viewsets.ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Oferta.objects.all()
        activas = self.request.query_params.get('activas', None)
        destacadas = self.request.query_params.get('destacadas', None)
        
        if activas:
            from django.utils import timezone
            now = timezone.now()
            queryset = queryset.filter(
                fecha_inicio__lte=now,
                fecha_fin__gte=now
            )
        
        if destacadas:
            queryset = queryset.filter(destacada=True)
            
        return queryset