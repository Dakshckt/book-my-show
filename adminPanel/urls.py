from django.urls import path
from . import views

urlpatterns = [
    path("city/" , views.cityFunc , name="cityFunc"),
    path("location/" , views.locationFunc , name="locationFunc"),
    path("theater/" , views.theaterFunc , name="theaterFunc"),
    path("screen/" , views.screenFunc , name="screenFunc"),
    path("movie-type/" , views.movieTypeFunc , name="movieTypeFunc"),
    path("movie/" , views.movieFunc , name="movieFunc"),
    path("seats/" , views.seatsFunc , name="seatsFunc"),
    path("movie-in-theater/" , views.movieInTheaterFunc , name="movieInTheaterFunc"),

    path("send-location/" , views.sendLocation , name="sendLocation"),
    path("send-theater/" , views.sendTheater , name="sendTheater"),
    path("send-screen/" , views.sendScreen , name="sendScreen"),
]