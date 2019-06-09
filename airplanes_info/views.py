from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import AircraftsData, AirportsData, BoardingPasses, Bookings, Flights, Seats, TicketFlights, Tickets
from .serializers import AircraftsDataSerializer, AirportsDataSerializer, \
    BoardingPassesSerializer, BookingsSerializer, FlightsSerializer, SeatsSerializer, TicketFlightsSerializer, \
    TicketsSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'aircrafts': reverse('aircrafts-list-create', request=request, format=format),
        'airports': reverse('airports-list-create', request=request, format=format),
        'bookings': reverse('bookings-list-create', request=request, format=format),
        'boarding-passes': reverse('boarding-passes-list-create', request=request, format=format),
        'flights': reverse('flights-list-create', request=request, format=format),
        'seats': reverse('seats-list-create', request=request, format=format),
        'ticket-flights': reverse('ticket-flights-list-create', request=request, format=format),
        'ticket': reverse('ticket-list-create', request=request, format=format),
    })


class AircraftsDataListCreateView(generics.ListCreateAPIView):
    queryset = AircraftsData.objects.all()
    serializer_class = AircraftsDataSerializer


class AircraftsDataRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AircraftsData.objects.all()
    serializer_class = AircraftsDataSerializer
    lookup_field = 'aircraft_code'


class AirportsDataListCreateView(generics.ListCreateAPIView):
    queryset = AirportsData.objects.all()
    serializer_class = AirportsDataSerializer


class AirportsDataRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirportsData.objects.all()
    serializer_class = AirportsDataSerializer
    lookup_field = 'airport_code'


class BookingsListCreateView(generics.ListCreateAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer


class BookingsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    lookup_field = 'book_ref'


class BoardingPassesListCreateView(generics.ListCreateAPIView):
    queryset = BoardingPasses.objects.all()
    serializer_class = BoardingPassesSerializer


class BoardingPassesRetrieveView(generics.RetrieveDestroyAPIView):
    queryset = BoardingPasses.objects.all()
    serializer_class = BoardingPassesSerializer
    multiple_lookup_fields = ['ticket_no', 'flight_id']

    def get_object(self):
        queryset = self.get_queryset()
        _filter = {}

        for field in self.multiple_lookup_fields:
            _filter[field] = self.kwargs[field]

        obj = queryset.filter(**_filter).first()
        return obj


class FlightsListCreateView(generics.ListCreateAPIView):
    queryset = Flights.objects.all()
    serializer_class = FlightsSerializer


class FlightsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flights.objects.all()
    serializer_class = FlightsSerializer
    lookup_field = 'flight_id'


class SeatsListCreateView(generics.ListCreateAPIView):
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializer


class SeatsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializer
    multiple_lookup_fields = ['aircraft_code', 'seat_no']

    def get_object(self):
        queryset = self.get_queryset()

        _filter = {}
        for field in self.multiple_lookup_fields:
            _filter[field] = self.kwargs[field]

        obj = queryset.filter(**_filter).first()
        return obj


class TicketFlightsListCreateView(generics.ListCreateAPIView):
    queryset = TicketFlights.objects.all()
    serializer_class = TicketFlightsSerializer


class TicketFlightsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketFlights.objects.all()
    serializer_class = TicketFlightsSerializer
    multiple_lookup_fields = ['ticket_no', 'flight']

    def get_object(self):
        queryset = self.get_queryset()
        _filter = {}

        for field in self.multiple_lookup_fields:
            _filter[field] = self.kwargs[field]

        obj = queryset.filter(**_filter).first()
        return obj


class TicketsListCreateView(generics.ListCreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer


class TicketsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    lookup_field = 'book_ref'
