from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('main', views.main, name="main"),
    path('getName', views.register, name="getName"),
    path('login', views.login, name="login"),
    path('changePass', views.changePass, name="changePass"),
]