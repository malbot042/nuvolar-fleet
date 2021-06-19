from django.urls import path, include

from fleet import views


urlpatterns = [

    # dummy test url
    path('check/', views.check, name='check'),

]
