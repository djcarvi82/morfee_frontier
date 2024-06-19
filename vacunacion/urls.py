from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='vac_inicio'),
    path('busqueda', views.busqueda, name='vac_busqueda'),
    path('busqueda/individual', views.jxSearchIndividual, name='vac_busqueda_simple'),

    path('agendar/<str:id>/', views.agendar, name='vac_agendar'),
]

