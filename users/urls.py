from django.urls import path
from . import views

urlpatterns = [
    path('admin/users', views.user_list, name='ad_user_list'),
    path('admin/user/select', views.user_preselect, name='ad_user_preselect'),
    path('admin/user/add', views.user_add, name='ad_user_add'),
    path('admin/user/add/staff', views.user_add_staff, name='ad_user_add_staff'),
    path('admin/user/edit/<int:id>/', views.user_edit, name='ad_user_edit'),
    path('admin/user/remove/<int:id>/', views.user_remove, name='ad_user_remove'),
    path('list', views.cli_user_list, name='ad_ucli_list'),
    path('add', views.cli_user_add, name='ad_ucli_add'),
    path('store', views.cli_user_add, name='ad_ucli_store'),
    path('edit/<int:id>/', views.cli_user_edit, name='ad_ucli_edit'),

    path('admin/clientes', views.cliente_list, name='ad_cliente_list'),
    path('admin/cliente/add', views.cliente_add, name='ad_cliente_add'),
    path('admin/cliente/edit/<int:id>/', views.cliente_edit, name='ad_cliente_edit'),
    path('admin/roles', views.rol_list, name='ad_rol_list'),
    path('admin/rol/add', views.rol_add, name='ad_rol_add'),
    path('admin/rol/edit/<int:id>/', views.rol_edit, name='ad_rol_edit'),
    path('admin/rol/remove/<int:id>/', views.rol_remove, name='ad_rol_remove'),
    path('admin/modulos', views.modulo_list, name='ad_modulo_list'),
    path('admin/modulo/add', views.modulo_add, name='ad_modulo_add'),
    path('admin/modulo/edit/<int:id>/', views.modulo_edit, name='ad_modulo_edit'),
    path('admin/modulo/remove/<int:id>/', views.modulo_remove, name='ad_modulo_remove'),
    path('admin/diccionario/<str:coleccion>/', views.get_diccionario, name="ad_diccionario"),
    path('admin/basic/import', views.basic_import_add, name='ad_basic_import'),
    path('admin/history/import', views.import_history, name='ad_history_import'),
    path('admin/basic/import/remove', views.import_delete_basic, name='ad_remove_import'),
    path('admin/reader', views.auto_reader_colection, name='ad_auto_reader'),
    path('admin/last/import', views.getLastImport, name='ad_last_import'),

    path('admin/codigo/import', views.getImport, name='ad_code_import'),
    path('ismael', views.ismael, name='ad_ismael'),
]
