from django.contrib import admin
from django.urls import include, path
from .views import listar_cardapios

urlpatterns = [
    path("cardapios/", listar_cardapios, name="listar_cardapios"),
]