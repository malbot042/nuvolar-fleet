from django.urls import path, include
from django.contrib.auth.views import LoginView as login, LogoutView as logout

from rest_framework import routers
from rest_framework.authtoken import views as token_views

from fleet import views


router = routers.DefaultRouter()
router.register(r'airport', views.AirportViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'flight', views.FlightViewSet)
router.register(r'report', views.ReportViewSet, basename='report')


urlpatterns = [

    # auth urls
    path('api-token-auth/', token_views.obtain_auth_token),
    # main nuvolar api urls
    path('', include(router.urls)),
]
