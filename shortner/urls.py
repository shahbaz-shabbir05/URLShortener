from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shortner.views import CreateShortURL, GetOriginalURL

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('url/new/', CreateShortURL.as_view(), name='create_short_url'),
    path('url/revert/', GetOriginalURL.as_view(), name='get_original_url'),
]
