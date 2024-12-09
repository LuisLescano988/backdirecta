from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet, SectorViewSet, CotizadorViewSet, CategoriaViewSet,
    TerminacionViewSet, ColorViewSet, RangoCantidadViewSet
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'sectores', SectorViewSet, basename='sector')
router.register(r'cotizadores', CotizadorViewSet, basename='cotizador')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'terminaciones', TerminacionViewSet, basename='terminacion')
router.register(r'colores', ColorViewSet, basename='color')
router.register(r'rangos-cantidad', RangoCantidadViewSet, basename='rango-cantidad')

urlpatterns = router.urls
