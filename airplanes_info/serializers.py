from django.urls import reverse
from rest_framework import serializers
from .models import AircraftsData, AirportsData, BoardingPasses, Bookings, Flights, FLIGHTS_STATUSES, Seats, \
    FARE_CONDITIONS, TicketFlights, Tickets
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.reverse import reverse


class ParameterisedHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    Represents the instance, or a property on the instance, using hyperlinking.
    lookup_fields is a tuple of tuples of the form:
        ('model_field', 'url_parameter')
    """
    lookup_fields = (('pk', 'pk'),)

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', self.lookup_fields)
        super(ParameterisedHyperlinkedIdentityField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        kwargs = {}
        for model_field, url_param in self.lookup_fields:
            kwargs[url_param] = getattr(obj, model_field)

        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class AircraftsDataSerializer(serializers.ModelSerializer):
    range = serializers.IntegerField(help_text="Максимальная дальность полета должна быть больше нуля (км)")
    url = ParameterisedHyperlinkedIdentityField(view_name='aircrafts-retrieve',
                                                lookup_fields=(('aircraft_code', 'aircraft_code'),),
                                                read_only=True)

    class Meta:
        model = AircraftsData
        fields = ('url', 'aircraft_code', 'model', 'range')

    def validate(self, data):
        if data['range'] <= 0:
            raise serializers.ValidationError("Максимальная дальность полета не может быть меньше или равной нулю")
        return data


class AirportsDataSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='airports-retrieve',
                                                lookup_fields=(('airport_code', 'airport_code'),),
                                                read_only=True)

    class Meta:
        model = AirportsData
        fields = ('url', 'airport_code', 'airport_name', 'city', 'coordinates', 'timezone')


class BookingsSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='bookings-retrieve',
                                                lookup_fields=(('book_ref', 'book_ref'),),
                                                read_only=True)

    class Meta:
        model = Bookings
        fields = ('url', 'book_ref', 'book_date', 'total_amount')


class FlightsSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='flights-retrieve',
                                                lookup_fields=(('flight_id', 'flight_id'),),
                                                read_only=True)
    departure_airport = serializers.PrimaryKeyRelatedField(queryset=AirportsData.objects.all())
    arrival_airport = serializers.PrimaryKeyRelatedField(queryset=AirportsData.objects.all())
    aircraft_code = serializers.PrimaryKeyRelatedField(queryset=AircraftsData.objects.all())
    status = serializers.CharField(help_text='Допустимы следующие статусы: Scheduled, On Time, Delayed, Departed, Arrived, Cancelled')

    class Meta:
        model = Flights
        fields = ('url', 'flight_id', 'flight_no', 'scheduled_departure',
                  'scheduled_arrival', 'departure_airport', 'arrival_airport',
                  'status', 'aircraft_code', 'actual_departure', 'actual_arrival')

    def validate(self, data):
        status_list = []
        [status_list.append(key) for key, val in FLIGHTS_STATUSES]

        if data['status'] not in status_list:
            raise serializers.ValidationError("Статус " + data['status'] + " не существует, пожалуйста выберите статус из предоставленного списка статусов")

        if data['scheduled_arrival'] < data['scheduled_departure']:
            raise serializers.ValidationError("Дата и время прибытия не может начинаться быстрее даты вылета")

        if data['actual_departure'] is not None and data['actual_arrival'] is not None:
            if data['actual_arrival'] < data['actual_departure']:
                raise serializers.ValidationError("Дата и время прибытия не может начинаться быстрее даты вылета")
        return data


class SeatsSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='seats-retrieve',
                                                lookup_fields=(('aircraft_code_id', 'aircraft_code'), ('seat_no', 'seat_no')),
                                                read_only=True)
    aircraft_code = serializers.PrimaryKeyRelatedField(queryset=AircraftsData.objects.all())
    fare_conditions = serializers.CharField(help_text='Допустимы следующие классы: Economy, Comfort, Business')

    class Meta:
        model = Seats
        fields = ('url', 'aircraft_code', 'seat_no', 'fare_conditions')

    def validate(self, data):
        fare_conditions = []
        [fare_conditions.append(key) for key, val in FARE_CONDITIONS]

        if data['fare_conditions'] not in fare_conditions:
            raise serializers.ValidationError("Класс " + data['fare_conditions'] + " не существует, пожалуйста выберите класс из предоставленного списка класов")
        return data


class BoardingPassesSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='boarding-passes-retrieve',
                                                lookup_fields=(('ticket_no_id', 'ticket_no'), ('flight_id', 'flight_id')),
                                                read_only=True)
    ticket_no = serializers.PrimaryKeyRelatedField(queryset=TicketFlights.objects.all())
    flight_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BoardingPasses
        fields = ('url', 'ticket_no', 'flight_id', 'boarding_no', 'seat_no')


class TicketFlightsSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='ticket-flights-retrieve',
                                                lookup_fields=(('ticket_no_id', 'ticket_no'), ('flight_id', 'flight')),
                                                read_only=True)
    fare_conditions = serializers.CharField(help_text='Допустимы следующие классы: Economy, Comfort, Business')

    class Meta:
        model = TicketFlights
        fields = ('url', 'ticket_no', 'flight_id', 'fare_conditions', 'amount')
        read_only_fields = ('flight_id', 'ticket_no')

    def validate(self, data):
        fare_conditions = []
        [fare_conditions.append(key) for key, val in FARE_CONDITIONS]

        if data['fare_conditions'] not in fare_conditions:
            raise serializers.ValidationError("Класс " + data['fare_conditions'] + " не существует, пожалуйста выберите класс из предоставленного списка класов")

        if data['amount'] <= 0:
            raise serializers.ValidationError("Стоимость перелета должна быть больше нуля")

        return data


class TicketsSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='ticket-retrieve',
                                                lookup_fields=(('book_ref_id', 'book_ref'),),
                                                read_only=True)

    class Meta:
        model = Tickets
        fields = ('url', 'ticket_no', 'book_ref_id', 'passenger_id', 'passenger_name', 'contact_data')
