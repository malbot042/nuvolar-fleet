from django.urls import path, include
from django.contrib.auth.views import LoginView as login, LogoutView as logout

from rest_framework import routers
from rest_framework.authtoken import views as auth_token_views

from fleet import views


router = routers.DefaultRouter()
router.register(r'airport', views.AirportViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'flight', views.FlightViewSet)
router.register(r'report', views.ReportViewSet, basename='report')


urlpatterns = [

    # auth urls
    path('token-auth/', auth_token_views.obtain_auth_token),
    path('accounts/login/', login.as_view(template_name='admin/login.html'), name='login'),
    path('accounts/logout/', logout.as_view(), name='logout'),

    # main nuvolar api urls
    path('', include(router.urls)),
]
