from rest_framework.viewsets import ModelViewSet
from .models import Producto, Sector, Cotizador, Categoria, Terminacion, Color, RangoCantidad
from .serializers import (ProductoSerializer, SectorSerializer, CotizadorSerializer, 
    CategoriaSerializer, TerminacionSerializer, ColorSerializer, RangoCantidadSerializer)

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class SectorViewSet(ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class CotizadorViewSet(ModelViewSet):
    queryset = Cotizador.objects.all()
    serializer_class = CotizadorSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class TerminacionViewSet(ModelViewSet):
    queryset = Terminacion.objects.all()
    serializer_class = TerminacionSerializer

class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class RangoCantidadViewSet(ModelViewSet):
    queryset = RangoCantidad.objects.all()
    serializer_class = RangoCantidadSerializer
