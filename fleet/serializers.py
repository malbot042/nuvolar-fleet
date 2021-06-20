from django.utils import timezone
from rest_framework import serializers

from fleet.models import Flight, Aircraft, Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

    @staticmethod
    def validate_departure_date(departure_date):
        if departure_date < timezone.now():
            raise serializers.ValidationError(
                "A flight can only be created for a future departure"
            )
        return departure_date


class ReportSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
