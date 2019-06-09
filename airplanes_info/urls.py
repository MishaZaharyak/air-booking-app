from django.urls import path
from airplanes_info import views


urlpatterns = [
    path('', views.api_root),
    # aircrafts
    path('aircrafts', views.AircraftsDataListCreateView.as_view(), name='aircrafts-list-create'),
    path('aircrafts/<aircraft_code>', views.AircraftsDataRetrieveView.as_view(), name='aircrafts-retrieve'),
    # airports
    path('airports', views.AirportsDataListCreateView.as_view(), name='airports-list-create'),
    path('airports/<airport_code>', views.AirportsDataRetrieveView.as_view(), name='airports-retrieve'),
    # bookings
    path('bookings', views.BookingsListCreateView.as_view(), name='bookings-list-create'),
    path('bookings/<book_ref>', views.BookingsRetrieveView.as_view(), name='bookings-retrieve'),
    # boarding-passes
    path('boarding-passes', views.BoardingPassesListCreateView.as_view(), name='boarding-passes-list-create'),
    path('boarding-passes/<ticket_no>/<flight_id>', views.BoardingPassesRetrieveView.as_view(), name='boarding-passes-retrieve'),
    # flights
    path('flights', views.FlightsListCreateView.as_view(), name='flights-list-create'),
    path('flights/<flight_id>', views.FlightsRetrieveView.as_view(), name='flights-retrieve'),
    # seats
    path('seats', views.SeatsListCreateView.as_view(), name='seats-list-create'),
    path('seats/<aircraft_code>/<seat_no>', views.SeatsRetrieveView.as_view(), name='seats-retrieve'),
    # ticket-flights
    path('ticket-flights', views.TicketFlightsListCreateView.as_view(), name='ticket-flights-list-create'),
    path('ticket-flights/<ticket_no>/<flight>', views.TicketFlightsRetrieveView.as_view(), name='ticket-flights-retrieve'),
    # ticket
    path('ticket', views.TicketsListCreateView.as_view(), name='ticket-list-create'),
    path('ticket/<book_ref>', views.TicketsRetrieveView.as_view(), name='ticket-retrieve'),
]
