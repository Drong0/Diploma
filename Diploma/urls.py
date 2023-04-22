from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, \
    SpectacularJSONAPIView
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('admin/', admin.site.urls),
                  path('api/', include('api.urls')),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  # Optional UI:
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='json'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
