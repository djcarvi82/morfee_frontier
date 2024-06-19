from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='ia_inicio'),
    path('search', views.search, name='ia_search'),
    path('consulta', views.consulta, name='ia_consulta'),
    path('cuenta', views.getCuenta, name='ia_cuenta'),
    path('subcuentas', views.getSubcuentas, name='ia_subcuentas'),
    path('sumatoria', views.getCuentaSuma, name='ia_suma'),
    path('sumatoria/texto', views.getTextoSuma, name='ia_suma_tx'),
    path('eps', views.getEPS, name='ia_eps'),
]
