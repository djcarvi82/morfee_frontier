from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='ase_inicio'),
    path('consulta', views.consulta, name='ase_consulta'),
    path('summary', views.summary, name='ase_summary'),
    path('import/list', views.import_list, name='ase_import_list'),
    path('import/add', views.import_add, name='ase_import_add'),
    path('import/history', views.import_history, name='ase_import_history'),
    path('import/delete', views.import_delete, name='ase_import_delete'),
    path('import/details', views.import_batch, name='ase_batch'),
    path('bdua/import/contributivo', views.import_bdua_con, name='ase_import_con'),

    path('contributivo/<str:section>/', views.cont_panel, name='ase_contributivo'),
    path('contributivo/dash/vue', views.cont_dash, name='ase_cont_dash'),

    path('subsidiado/<str:section>/', views.sub_panel, name='ase_subsidiado'),
    path('subsidiado/dash/vue', views.sub_dash, name='ase_sub_dash'),

    path('sisben/<str:section>/', views.sisben_panel, name='ase_sisben'),
    path('sisben/dash/vue', views.sisben_dash, name='ase_sisben_dash'),

    path('lma/<str:section>/', views.lma_panel, name='ase_lma'),

    path('import/temo', views.temo, name='temo'),

    path('georreferenciacion', views.geoLocation, name='ase_location_map'),
    path('geodata', views.getGeodata, name='ase_geodata'),
    path('geodata/by/id', views.getGeodataId, name='ase_geodata_id'),
    path('geodata/proximity', views.getProximity, name='ase_proximity'),
    path('grupos', views.getGrupo, name='ase_grupos'),
    path('geocode', views.tpl_geocode, name='ase_geocode'),
    path('manager', views.tpl_manager_geo, name='ase_manager'),
    path('manager/red', views.getRedNativa),
    path('manager/coords/save', views.saveCoord),
]
