from django.urls import path
from . import views

urlpatterns = [
    # path('', views.inicio, name='serv_inicio'),
    path('', views.hc_show, name='serv_inicio'),
    path('hc', views.hc_show, name='serv_hc_show'),
    path('hc/add', views.hc_register, name='serv_hc_add'),
    path('hc/search/doc', views.hc_search_doc, name='serv_doc'),
    path('hc/search/consulta', views.hc_search_consulta, name='serv_consulta'),
    path('hc/save', views.hc_save_doc, name='serv_hc_save'),


    
    # path('dash/<str:section>/', views.dashboards, name='retec_dash'),

    # path('mng/raw', views.raw_facet, name='retec_raw'),
    # path('piramide/data', views.pyr_data, name='retec_pyr_data'),
]
