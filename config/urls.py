from django.contrib import admin
from django.urls import path
from .api import api

from cardapio.views import (
    escolha_perfil,
    usuario_comum,
    login_nutricionista,
    dashboard_nutricionista,
    sair,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),

    path("", escolha_perfil, name="escolha_perfil"),
    path("usuario/", usuario_comum, name="usuario_comum"),
    path("login/", login_nutricionista, name="login_nutricionista"),
    path("dashboard/", dashboard_nutricionista, name="dashboard_nutricionista"),
    path("sair/", sair, name="sair"),
]