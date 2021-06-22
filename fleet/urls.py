from django.urls import path, include
from django.contrib.auth import views as auth_views

from rest_framework import routers
from rest_framework.authtoken import views as token_views
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from fleet import views


schema_view = get_schema_view(
   openapi.Info(
      title="Nuvolar Fleet API",
      default_version='v1',
      description="Nuvolar Fleet API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="malbot042@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

router = routers.DefaultRouter()
router.register(r'airport', views.AirportViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'flight', views.FlightViewSet)
router.register(r'report', views.ReportViewSet, basename='report')

urlpatterns = [
    # swagger api
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # auth urls
    path('api-token-auth/', token_views.obtain_auth_token),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = "admin/login.html")),
    # main nuvolar api urls
    path('', include(router.urls)),
]
