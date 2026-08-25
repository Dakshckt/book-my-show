from . import views
from django.urls import path

urlpatterns = [
    path("login/" , views.loginFunc , name="loginFunc"),
    path("signup/" , views.signupFunc , name="signupFunc"),
    path("logout/" , views.logoutFunc , name="logoutFunc"),
    path("home/" , views.homeFunc , name="homeFunc")
]