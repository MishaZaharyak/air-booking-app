from django.db import models
from django.utils import translation
from django.contrib.postgres.fields import JSONField

FLIGHTS_STATUSES = (
    ('Scheduled', 'Scheduled'),
    ('On Time', 'On Time'),
    ('Delayed', 'Delayed'),
    ('Departed', 'Departed'),
    ('Arrived', 'Arrived'),
    ('Cancelled', 'Cancelled')
)

FARE_CONDITIONS = (
    ('Economy', 'Economy'),
    ('Comfort', 'Comfort'),
    ('Business', 'Business')
)


class AircraftsData(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = JSONField()
    range = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aircrafts_data'

    def lang(self):
        return self.model.get(translation.get_language(), 'No translate for current language')

    def __str__(self):
        return self.lang()


class AirportsData(models.Model):
    airport_code = models.CharField(primary_key=True, max_length=3)
    airport_name = JSONField()
    city = JSONField()
    coordinates = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'airports_data'

    def lang(self):
        return self.airport_name.get(translation.get_language(), 'No translate for current language')

    def __str__(self):
        return self.lang()


class BoardingPasses(models.Model):
    ticket_no = models.ForeignKey('TicketFlights', on_delete=models.CASCADE, db_column='ticket_no', primary_key=True)
    flight_id = models.IntegerField()
    boarding_no = models.IntegerField()
    seat_no = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'bookings'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(AirportsData, on_delete=models.CASCADE, db_column='departure_airport', related_name='departure_airport')
    arrival_airport = models.ForeignKey(AirportsData, on_delete=models.CASCADE, db_column='arrival_airport', related_name='arrival_airport')
    status = models.CharField(max_length=20)
    aircraft_code = models.ForeignKey(AircraftsData, on_delete=models.CASCADE, db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)


class Seats(models.Model):
    aircraft_code = models.ForeignKey(AircraftsData, on_delete=models.CASCADE, db_column='aircraft_code', primary_key=True)
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)


class TicketFlights(models.Model):
    ticket_no = models.ForeignKey('Tickets', on_delete=models.CASCADE, db_column='ticket_no', primary_key=True)
    flight = models.ForeignKey(Flights, on_delete=models.CASCADE)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight'),)


class Tickets(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey(Bookings, on_delete=models.CASCADE, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'
