from django.http.response import HttpResponse
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated

from fleet.models import Airport, Aircraft, Flight
from fleet.serializers import (
    AirportSerializer,
    AircraftSerializer,
    FlightSerializer,
    ReportSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = ReportSerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return None
