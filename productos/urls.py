from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet,
    SectorViewSet,
    CategoriaViewSet,
    ColorViewSet,
    MaterialViewSet,
    TamanioPredefinidoViewSet,
    TerminacionViewSet,
    TipoClienteViewSet,
    OfertaViewSet
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'sectores', SectorViewSet, basename='sector')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'colores', ColorViewSet, basename='color')
router.register(r'materiales', MaterialViewSet, basename='material')
router.register(r'tamanios', TamanioPredefinidoViewSet, basename='tamanio')
router.register(r'terminaciones', TerminacionViewSet, basename='terminacion')
router.register(r'tipos-cliente', TipoClienteViewSet, basename='tipo-cliente')
router.register(r'ofertas', OfertaViewSet, basename='oferta')

urlpatterns = router.urls