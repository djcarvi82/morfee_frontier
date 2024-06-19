"""morfee_frontier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='morfee_frontier/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.CustomChangePWDView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    path('', views.inicio, name='inicio'),
    path('diccionario', views.diccionario, name='ad_diccionario'),
    # path('clientes', views.clientes, name='ad_clientes_vue'),
    # path('modulos', views.modulos, name='ad_modulos_vue'),
    path('diccionario/build', views.infoForDictio, name='ad_info_dictio'),
    path('diccionario/collections', views.getCollections, name='ad_collections'),
    path('diccionario/collection', views.getCollection, name='ad_collection'),
    path('diccionario/update', views.updateField, name='ad_dictio_edit'),
    path('diccionario/cliente', views.dicsOfUser, name='ad_dictio_client'),
    path('users/', include('users.urls')),
    path('aseguramiento/', include('aseguramiento.urls')),
    path('vacunacion/', include('vacunacion.urls')),
    path('reservas/', include('reservas.urls')),
    path('auditorias/', include('auditorias.urls')),
    path('financiero/', include('financiero.urls')),
    path('servicios/', include('servicios.urls')),
    path('ghg/', include('ghg.urls')),
    path('inte_', views.inicio, name='inte_inicio'),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
