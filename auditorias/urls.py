from django.urls import path
from . import views

urlpatterns = [
    path('', views.resumen, name='audit_inicio'),
    path('asignacion', views.inicio, name='audit_asign'),
    path('pooja', views.pooja, name='audit_pooja'),
    path('daniel', views.prueba_s3, name='audit_daniel'),
    path('import', views.importea, name='audit_import'),
    path('import/glosa', views.import_glosa, name='audit_import_glo'),
    path('import/us', views.import_us, name='audit_import_us'),
    path('import/ac', views.import_ac, name='audit_import_ac'),
    path('import/ap', views.import_ap, name='audit_import_ap'),
    path('import/af', views.import_af, name='audit_import_af'),
    path('import/ah', views.import_ah, name='audit_import_ah'),
    path('import/am', views.import_am, name='audit_import_am'),
    path('import/at', views.import_at, name='audit_import_at'),
    path('import/au', views.import_au, name='audit_import_au'),

    path('import/alt', views.importAlt, name='audit_import_alt'),
    path('kpi', views.kpi, name='audit_kpi'),
    path('resumen', views.resumen, name='audit_resumen'),
    path('consulta', views.consulta, name='audit_consulta'),
    path('general', views.general, name='audit_general'),
    path('facturacion', views.facturacion, name='audit_factura'),
    path('glosa', views.glosaTemplate, name='audit_glosa'),
    path('estado', views.estadoTemplate, name='audit_estado'),
    path('vue/general', views.getGeneralVue, name='audit_vue_gen'),
    path('vue/facturas', views.getFacturasVue, name='audit_vue_fac'),
    path('vue/details', views.getDetailsVue, name='audit_vue_det'),
    path('vue/facturas/fecha', views.getFacturasXFecha, name='audit_vue_dates'),
    path('vue/facturas/point', views.getFacturasPoint, name='audit_vue_point'),
    path('vue/facturas/asignacion', views.getAsignacion, name='audit_vue_asign'),
    path('vue/factura', views.getFacturaRef, name='audit_vue_ref'),
    path('vue/factura/edit/one', views.addOneTecnico, name='audit_edit_one'),
    path('sispro', views.sispro, name='audit_sispro'),
    path('actas', views.actas, name='audit_actas'),
    path('qr/list', views.qrList, name='audit_qrlist'),
    path('qr', views.qr_example, name='audit_qr'),
    path('vue/acta', views.vueActaRef, name='audit_acta_ref'),  # CHECK
    path('vue/acta/glosa/cross', views.vueActaCross, name='audit_acta_cross'),
    path('vue/acta/save', views.vueSaveActa, name='audit_acta_save'),   # CHECK
    path('vue/acta/save/edit', views.vueSaveEditActa, name='audit_acta_edit'),
    path('vue/acta/list', views.vueListActasQR, name='audit_acta_list'),    # CHECK
    path('vue/acta/<str:code>', views.vueImageQR, name='audit_acta_img'),   # QR CODE
    path('vue/qr/list', views.vueListQR, name='audit_vue_list'),
    path('vue/qr/list/save', views.vueSaveQR, name='audit_qr_save'),
    path('vue/qr/<str:code>/', views.vueFacturaQR, name='audit_vue_fac_one'),
    path('vue/codex', views.vueCodex, name='audit_codex'),  # CHECK
    path('vue/search/fac', views.vueSearchFac, name='audit_search'),    # CHECK
    path('vue/cifras', views.vueCifras, name='audit_cifras'),
    path('vue/cifras/periodos', views.vuePeriodos, name='audit_cifras_per'),
    path('vue/cifras/social', views.vueSocial, name='audit_cifras_soc'),
    path('vue/cifras/ipss', views.allEntities, name='audit_ipss'),
    path('vue/cifras/regimen', views.vueRegimen, name='audit_cifras_regimen'),
    path('vue/cifras/case', views.vueCase, name='audit_cifras_case'),
    path('vue/cifras/case/select/bar', views.vueCaseSelectBar),
    path('vue/cifras/conciliacion', views.vueConciliacion, name='audit_cifras_concilia'),
    path('vue/cifras/conciliacion/slice/bar', views.vueConciliacionBar, name='audit_cifras_concilia'),
    path('vue/cifras/conciliacion/slice', views.vueConciliaSlice),
    
    path('vue/glosa/stat', views.codeglosa, name='audit_stat'),
    path('vue/glosa/stat/detail', views.detalleglosa, name='audit_detail'),
    path('vue/estado', views.estadoTecnica, name='audit_status'),
    path('vue/estado/init', views.estadoTecnicaInit),
    path('vue/estado/select/bar', views.estadoTecnicaSlice),
    path('vue/filtros', views.getFiltros, name='audit_filtros'),

    path('vue/kpi', views.kpi_periodos, name='audit_kpi_per'),  #KPI
    path('vue/kpi/control', views.kpi_control),
    path('vue/kpi/control/fechas', views.kpi_control_fechas),
]

    # path="{% url 'audit_codex' %}" 
    # pathbase="{% url 'audit_acta_ref' %}"
    # pathsearch="{% url 'audit_search' %}" 
    # pathlist="{% url 'audit_acta_list' %}"
    # pathsave="{% url 'audit_acta_save' %}"

    # path('dashboards/<str:section>/', views.dashboards, name='retec_dashboard'),
    # path('contratos/<str:section>/', views.cont_panel, name='retec_contratos'),
    # path('autorizaciones/<str:section>/', views.aut_panel, name='retec_autorizaciones'),
    # path('facturas/<str:section>/', views.fac_panel, name='retec_facturas'),
    # path('pagos/<str:section>/', views.pag_panel, name='retec_pagos'),
    # path('incapacidades/<str:section>/', views.inca_panel, name='retec_incapacidades'),
    # path('fragmentacion', views.fragmentation, name='retec_fragment'),
    # path('info/periodos', views.getPeriodos, name='retec_periodos'),
    # path('info/orphan', views.getCreatedOrphan, name='retec_orphan'),
    # path('mng/facet', views.mng_facet, name='retec_mng_facet'),
    # path('mng/group', views.mng_group, name='retec_mng_group'),
    # path('mng/group/multiple', views.mng_group_multiple, name='retec_mng_group_multiple'),
    # path('mng/schema', views.mng_schema, name='retec_mng_schema'),
    # path('mng/fixed/crx', views.fixedPeriodo, name='retec_mng_crx'),
