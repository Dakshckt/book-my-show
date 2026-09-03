from django.urls import path
from . import views

urlpatterns = [
    path("home/" , views.clientHomeFunc , name="clientHomeFunc"),
    path("movie/<str:link>/" , views.singleMovieFunc , name="singleMovieFunc"),
    path("send-movies/" , views.sendMovieFunc , name="sendMovieFunc"),
    path("send-date/" , views.sendDateFunc , name="sendDateFunc"),
    path("send-shows/" , views.sendShowsFunc , name="sendShowsFunc"),
    path("movie-in-theater/<str:link>/" , views.movieInTheater , name="movieInTheater"),
    path("seats/<str:show_id>/<str:show_timing_id>/<str:date_selected>/" , views.seatSelectionFunc , name="seatSelectionFunc"),
    path("my-booking/" , views.myBookingFunc , name="myBookingFunc")
]
