from django.urls import path
from . import views

urlpatterns = [
    path('', views.template_inicio, name='ghg_inicio'),  # compras
    path('import', views.template_import, name='ghg_import'),
    path('dataini', views.dataini, name='ghg_dataini'),
]
