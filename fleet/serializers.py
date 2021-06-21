from datetime import date
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

    def validate_departure_date(self, departure_date):
        if departure_date < timezone.now():
            raise serializers.ValidationError(
                "departure date can only be created for a future departure"
            )
        return departure_date

    def validate_arrival_date(self, arrival_date):
        try:
            naive_date = timezone.datetime.strptime(
                self.initial_data['departure_date'],
                "%Y-%m-%dT%H:%M:%S"
            )
        except:
            naive_date = timezone.datetime.strptime(
                self.initial_data['departure_date'],
                "%Y-%m-%dT%H:%M"
            )
        departure_date = timezone.make_aware(naive_date)
        if arrival_date < departure_date:
            raise serializers.ValidationError(
                "arrival date can not be created for past departure date"
            )
        return arrival_date

    class Meta:
        model = Flight
        fields = '__all__'
