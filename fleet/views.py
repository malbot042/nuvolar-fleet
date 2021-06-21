from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
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

    def get_queryset(self):
        qs = super().get_queryset()

        departure_airport = self.request.query_params.get('departure_airport')
        arrival_airport = self.request.query_params.get('arrival_airport')

        if departure_airport:
            qs = qs.filter(departure_airport=departure_airport)
        if arrival_airport:
            qs = qs.filter(arrival_airport=arrival_airport)

        departure_date = self.request.query_params.get('departure_date')
        arrival_date = self.request.query_params.get('arrival_date')

        if departure_date:
            qs = qs.filter(departure_date__gte=departure_date)
        if arrival_date:
            qs = qs.filter(arrival_date__gte=arrival_date)

        return qs

class ReportViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Flight.objects.all()

        departure_date = self.request.query_params.get('departure_date')
        arrival_date = self.request.query_params.get('arrival_date')

        if departure_date:
            qs = qs.filter(departure_date__gte=departure_date)
        if arrival_date:
            qs = qs.filter(arrival_date__lte=arrival_date)

        return qs

    def list(self, request):
        # import ipdb; ipdb.set_trace()
        data = {}
        qs = self.get_queryset().order_by('id')
        for flight in qs:
            delta_time = (flight.arrival_date - flight.departure_date).total_seconds() / 60
            if flight.departure_airport.icao not in data.keys():
                icao_flights = {
                    'flights': 1,
                    'total': 0,
                    'average': 0,
                    'aircrafts': {},
                }
                data[flight.departure_airport.icao] = icao_flights
            else:
                data[flight.departure_airport.icao]['flights'] += 1
            # update the aircraft data structure
            aircraft = flight.aircraft.serial_number if flight.aircraft else 'Unknow'
            if aircraft not in icao_flights['aircrafts'].keys():
                icao_flights['aircrafts'][aircraft] = delta_time
            else:
                icao_flights['aircrafts'][aircraft] += delta_time
            icao_flights['total'] += delta_time
        total = data[flight.departure_airport.icao]['total']
        flights = data[flight.departure_airport.icao]['flights']
        data[flight.departure_airport.icao]['average'] = total / flights
        return Response(data)