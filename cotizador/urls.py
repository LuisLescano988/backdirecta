from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoClickViewSet,
    CargoPorBajadaViewSet,
    CalidadViewSet,
    TipoImpresionViewSet,
    ConfiguracionCotizadorOffsetViewSet,
    ConfiguracionCotizadorDigitalViewSet,
    ConfiguracionCotizadorGranFormatoViewSet,
    TipoPapelViewSet,
    CostoTerminacionViewSet
)

router = DefaultRouter()

# Configuraciones básicas
router.register(r'tipos-click', TipoClickViewSet)
router.register(r'cargos-bajada', CargoPorBajadaViewSet)
router.register(r'calidades', CalidadViewSet)
router.register(r'tipos-impresion', TipoImpresionViewSet)
router.register(r'tipos-papel', TipoPapelViewSet)
router.register(r'costos-terminacion', CostoTerminacionViewSet)

# Configuradores por tipo
router.register(r'configuracion-offset', ConfiguracionCotizadorOffsetViewSet)
router.register(r'configuracion-digital', ConfiguracionCotizadorDigitalViewSet)
router.register(r'configuracion-gran-formato', ConfiguracionCotizadorGranFormatoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Endpoints:
# GET/POST/PUT/DELETE /api/v1/cotizador/tipos-click/
# GET/POST/PUT/DELETE /api/v1/cotizador/cargos-bajada/
# GET/POST/PUT/DELETE /api/v1/cotizador/calidades/
# GET/POST/PUT/DELETE /api/v1/cotizador/tipos-impresion/
# GET/POST/PUT/DELETE /api/v1/cotizador/tipos-papel/
# GET/POST/PUT/DELETE /api/v1/cotizador/costos-terminacion/
# GET/POST/PUT/DELETE /api/v1/cotizador/configuracion-offset/
# GET/POST/PUT/DELETE /api/v1/cotizador/configuracion-digital/
# GET/POST/PUT/DELETE /api/v1/cotizador/configuracion-gran-formato/

# Endpoints adicionales para consultas específicas:
# GET /api/v1/cotizador/configuracion-offset/por_producto/?producto_id=X
# GET /api/v1/cotizador/configuracion-digital/por_producto/?producto_id=X
# GET /api/v1/cotizador/configuracion-gran-formato/por_producto/?producto_id=X