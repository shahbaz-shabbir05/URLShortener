from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from shortner.views import HelloView, CreateShortURL, GetOriginalURL

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('CreateShortURL/', CreateShortURL.as_view(), name='create_short_url'),
    path('GetOriginalURL/', GetOriginalURL.as_view(), name='get_origina_URL'),
]