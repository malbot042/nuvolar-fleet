"""
This is the main Nuvolar Fleet Model Module
"""

from django.db import models


class Airport(models.Model):
    """
    Airport: ICAO code
    """
    icao = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.icao}"


class Aircraft(models.Model):
    """
    Aircraft: serial number & manufacturer.
    """

    serial_number = models.CharField(
        max_length=20,
        unique=True,
    )
    manufacturer = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return f"{self.manufacturer}: {self.serial_number}"


class Flight(models.Model):
    """
    A flight is:
        - A departure date and airport
        - An arrival date and airport
    """

    departure_date = models.DateTimeField()
    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.DO_NOTHING,
        related_name='departura_flight'
    )

    arrival_date = models.DateTimeField()
    arrival_airport = models.ForeignKey(
        Airport,
        on_delete=models.DO_NOTHING,
        related_name='arrival_flight'
    )

    aircraft = models.ForeignKey(
        Aircraft,
        related_name='flights',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return \
            f"{self.id} | " \
            f"{self.departure_airport} : {self.departure_date} | " \
            f"{self.arrival_airport} : {self.arrival_date} | " \
            f"{self.aircraft}"
