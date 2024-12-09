# from django.urls import path
# from .views import google_login, CookieTokenRefreshView, LogoutView

# urlpatterns = [
#     path('google-login/', google_login, name='google_login'),
#     path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]
from django.urls import path
from .views import GoogleLoginView, TokenRefreshView

urlpatterns = [
    path('api/auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]