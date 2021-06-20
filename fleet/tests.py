from fleet.models import Aircraft, Airport, Flight
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthTokenTest(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        user = User.objects.create(
            username='root',
            password='Nuvolar-API-password',
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return self


class AirportPostTest(AuthTokenTest):
    """
    Simple post for a new aiport
    """
    def setUp(self) -> None:
        super().setUp()
        return self

    def test_airport_post(self):
        response = self.client.post(
            reverse('airport-list'),
            {'icao': 'NU00'},
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


class AirCraftDeleteTest(AuthTokenTest):
    """
    Simple Aircraft delete test
    """
    def setUp(self) -> None:
        super().setUp()
        self.aircraft = Aircraft.objects.create(
            serial_number='TEST',
            manufacturer='TEST'
        )
        return self

    def test_aircraft_delete(self):
        response = self.client.delete(
            reverse('aircraft-detail', args=[self.aircraft.id]),
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class FlightErrorTest(AuthTokenTest):
    """
    Simple Flight Error test: check if we can add a flight
    for a past date
    """
    def setUp(self) -> None:
        super().setUp()
        self.airport = Airport.objects.create(icao='TEST')
        self.aircraft = Aircraft.objects.create(
            serial_number='TEST',
            manufacturer='TEST'
        )
        return self

    def test_flight_post_err(self):
        response = self.client.post(
            reverse('flight-list'),
            {
                "departure_date": "2020-06-20T10:00:00Z",
                "arrival_date": "2020-06-21T12:00:00Z",
                "departure_airport": self.airport.id,
                "arrival_airport": self.airport.id,
                "aircraft": None
            },
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class FlightFilterTest(AuthTokenTest):
    """
    Dummy Flight Test filter
    """

    def setUp(self) -> None:
        super().setUp()

        self.airport = Airport.objects.create(icao='TEST')
        self.aircraft = Aircraft.objects.create(
            serial_number='TEST',
            manufacturer='TEST'
        )

        self.flight = Flight.objects.create(
            departure_date='2012-01-01T00:00:00Z',
            arrival_date='2012-01-02T00:00:00Z',
            departure_airport=self.airport,
            arrival_airport=self.airport
        )

    def test_filter_err(self):
        url = reverse('flight-list')
        url += '?departure_date=2020-01-01T00:00Z'
        response = self.client.get(
            url,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(),[])

    def test_filter_ok(self):
        url = reverse('flight-list')
        url += '?departure_date=2012-01-01T00:00Z'
        response = self.client.get(
            url,
            format='json'
        )
        data = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(data), 1)