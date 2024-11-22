from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('productos.urls')),
    path('api/v1/', include('cotizador.urls')),
]