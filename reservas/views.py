from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
from mf_consulta.models import Consulta
from datetime import date
import json
# from bson.code import Code

def createConsulta(name, cole, cla, cli, user):
    print('Generando consulta: ' + name)
    try:
        c = Consulta.objects.filter(nombre=name, coleccion=cole, cliente_id=cli, user_id=user).get()
        c.clave = cla
        c.estado = 'reopen'
        c.created_at = date.today()
        c.save()
        return c
    except Consulta.DoesNotExist:
        cn = Consulta()
        cn.nombre = name
        cn.coleccion = cole
        cn.clave = cla
        cn.estado = 'open'
        cn.cliente_id = cli
        cn.user_id = user
        cn.save()
        return cn

def getConsulta(request):
    keycode = request.POST.get('clave') if request.POST.get('clave') else ''
    name = request.POST.get('consulta')
    cli = request.user.cliente_id if request.user.cliente_id else 0
    uid = request.user.id
    print('Clave: ' + keycode + ', consulta: ' + name)
    try:
        c = Consulta.objects.filter(nombre=name, clave=keycode, cliente_id=cli, user_id=uid).get() if keycode != '' else Consulta.objects.filter(nombre=name, cliente_id=cli, user_id=uid).get()
        contenido = json.loads(c.contenido) if c.contenido else []
        print('Consulta encontrada')
        rs = {'nombre': c.nombre, 'coleccion': c.coleccion, 'contenido': contenido, 'clave': c.clave, 'estado': c.estado, 'created_at': c.created_at}
        return JsonResponse(rs)
    except Consulta.DoesNotExist:
        print('No existe la consulta')
        rs = {'nombre': name, 'coleccion': '', 'contenido': '', 'clave': keycode, 'estado': 'void', 'created_at': str(date.today())}
        return JsonResponse(rs)


# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'reservas/panel_modulo.html')

@login_required(login_url='/login/')
def piramide(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'reservas/piramide.html', {'clienteId': clienteId, 'cliente': cliente})

@login_required(login_url='/login/')
def fragmentation(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    if request.user.cliente:
        clienteId = str(request.user.cliente.id)
        cliente = request.user.cliente.cliente
    return render(request, 'reservas/fragmentation.html', {'masterId': clienteId, 'clienteId': clienteId, 'cliente': cliente})

@login_required(login_url='/login/')
def custom_1(request):
    return render(request, 'reservas/clientes/custom_1.html')

@login_required(login_url='/login/')
def custom_2(request):
    return render(request, 'reservas/clientes/custom_2.html')

# ***********************************************************
# ******************** SECTION CONTRATOS ********************
# ***********************************************************

def cont_panel(request, section):
    if section == 'inicio':
        return cont_inicio(request)
    elif section == 'table':
        return cont_table(request)
    elif section == 'import':
        return cont_import(request)
    elif section == 'dash':
        return cont_dash(request)
    elif section == 'extra':
        return cont_extra(request)

def cont_inicio(request):
    coleccion = 'retec_contratos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_contratos_0'
    return render(request, 'reservas/contratos/cont_inicio.html', {'coleccion': coleccion})

def cont_import(request):
    coleccion = 'retec_contratos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_contratos_0'
    return render(request, 'reservas/contratos/cont_import.html', {'coleccion': coleccion})

def cont_table(request):
    coleccion = 'retec_contratos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_contratos_0'
    return render(request, 'reservas/contratos/cont_table.html', {'coleccion': coleccion})

def cont_dash(request):
    coleccion = 'retec_contratos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_contratos_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_base': [{"$group": {"_id": "", "base": {"$sum": "$bas"}}}],
            'facet_actual': [{"$group": {"_id": "", "actual": {"$sum": "$act"}}}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_pre': [{"$group": {"_id": "$idp"}}],
            'facet_doc': [{"$sortByCount": "$tpp"}],
            # 'facet_suma': [{"$project": {"base": {"$sum": "$bas"}, "actual": {"$sum": "$act"}}}],
            # {"$group": {"_id": "$depmun", "total": {"$sum": 1}}}
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def cont_extra(request):
    coleccion = 'retec_contratos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_contratos_0'
    mongo = Mongo(coleccion)
    datos = mongo.getCliente().count()
    mongo.close()
    return HttpResponse(datos, content_type="application/json")


# ****************************************************************
# ******************** SECTION AUTORIZACIONES ********************
# ****************************************************************
def aut_panel(request, section):
    if section == 'inicio':
        return aut_inicio(request)
    elif section == 'table':
        return aut_table(request)
    elif section == 'import':
        return aut_import(request)
    elif section == 'dash':
        return aut_dash(request)

def aut_inicio(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    return render(request, 'reservas/autorizaciones/aut_inicio.html', {'coleccion': coleccion})

def aut_table(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    return render(request, 'reservas/autorizaciones/aut_table.html', {'coleccion': coleccion})

def aut_import(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    return render(request, 'reservas/autorizaciones/aut_import.html', {'coleccion': coleccion})

def aut_dash(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_amb': [{"$sortByCount": "$amb"}],
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vbs': [{"$project": {"_id": 0, "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vbs"}}}],
            'facet_vac': [{"$group": {"_id": None, "n": {"$sum": "$vac"}}}],
            'facet_vpm': [{"$project": {"_id": 0, "n_vpm": {"$convert": {"input": "$vpm", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vpm"}}}],
            'facet_doc': [{"$sortByCount": "$tus"}],
            # 'facet_pmx': [{"$group": {"_id": None, "n": {"$sum": "$pmx"}}}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


# **********************************************************
# ******************** SECTION FACTURAS ********************
# **********************************************************
def fac_panel(request, section):
    if section == 'inicio':
        return fac_inicio(request)
    elif section == 'table':
        return fac_table(request)
    elif section == 'import':
        return fac_import(request)
    elif section == 'dash':
        return fac_dash(request)

def fac_inicio(request):
    return render(request, 'reservas/facturas/fac_inicio.html')

def fac_table(request):
    coleccion = 'retec_facturas_' + str(request.user.cliente.id) if request.user.cliente else 'retec_facturas_0'
    return render(request, 'reservas/facturas/fac_table.html', {'coleccion': coleccion})

def fac_import(request):
    coleccion = 'retec_facturas_' + str(request.user.cliente.id) if request.user.cliente else 'retec_facturas_0'
    return render(request, 'reservas/facturas/fac_import.html', {'coleccion': coleccion})

def fac_dash(request):
    coleccion = 'retec_facturas_' + str(request.user.cliente.id) if request.user.cliente else 'retec_facturas_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_amb': [{"$sortByCount": "$amb"}],
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_tra': [{"$sortByCount": "$tra"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vbs': [{"$project": {"_id": 0, "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vbs"}}}],
            'facet_vac': [{"$group": {"_id": None, "n": {"$sum": "$vac"}}}],
            'facet_vpm': [{"$project": {"_id": 0, "n_vpm": {"$convert": {"input": "$vpm", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vpm"}}}],
            'facet_vdo': [{"$project": {"_id": 0, "n_vdo": {"$convert": {"input": "$vdo", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vdo"}}}],
            'facet_vgl': [{"$project": {"_id": 0, "n_vgl": {"$convert": {"input": "$vgl", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vgl"}}}],
            'facet_gde': [{"$project": {"_id": 0, "n_gde": {"$convert": {"input": "$gde", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_gde"}}}],
            'facet_doc': [{"$sortByCount": "$tus"}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


# *******************************************************
# ******************** SECTION PAGOS ********************
# *******************************************************
def pag_panel(request, section):
    if section == 'inicio':
        return pag_inicio(request)
    elif section == 'table':
        return pag_table(request)
    elif section == 'import':
        return pag_import(request)
    elif section == 'dash':
        return pag_dash(request)

def pag_inicio(request):
    return render(request, 'reservas/pagos/pag_inicio.html')

def pag_table(request):
    coleccion = 'retec_pagos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_pagos_0'
    return render(request, 'reservas/pagos/pag_table.html', {'coleccion': coleccion})

def pag_import(request):
    coleccion = 'retec_pagos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_pagos_0'
    return render(request, 'reservas/pagos/pag_import.html', {'coleccion': coleccion})

def pag_dash(request):
    coleccion = 'retec_pagos_' + str(request.user.cliente.id) if request.user.cliente else 'retec_pagos_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_amb': [{"$sortByCount": "$amb"}],
            'facet_tra': [{"$sortByCount": "$tra"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vdo': [{"$group": {"_id": None, "n": {"$sum": "$vdo"}}}],
            'facet_gde': [{"$group": {"_id": None, "n": {"$sum": "$gde"}}}],
            'facet_vpbs': [{"$group": {"_id": None, "n": {"$sum": "$vpbs"}}}],
            'facet_vpac': [{"$group": {"_id": None, "n": {"$sum": "$vpac"}}}],
            'facet_vppm': [{"$group": {"_id": None, "n": {"$sum": "$vppm"}}}],
            'facet_doc': [{"$sortByCount": "$tus"}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


# ***************************************************************
# ******************** SECTION INCAPACIDADES ********************
# ***************************************************************
def inca_panel(request, section):
    if section == 'inicio':
        return inca_inicio(request)
    elif section == 'table':
        return inca_table(request)
    elif section == 'import':
        return inca_import(request)
    elif section == 'dash':
        return inca_dash(request)

def inca_inicio(request):
    return render(request, 'reservas/incapacidades/inca_inicio.html')

def inca_table(request):
    coleccion = 'retec_incapacidades_' + str(request.user.cliente.id) if request.user.cliente else 'retec_incapacidades_0'
    return render(request, 'reservas/incapacidades/inca_table.html', {'coleccion': coleccion})

def inca_import(request):
    coleccion = 'retec_incapacidades_' + str(request.user.cliente.id) if request.user.cliente else 'retec_incapacidades_0'
    return render(request, 'reservas/incapacidades/inca_import.html', {'coleccion': coleccion})

def inca_dash(request):
    coleccion = 'retec_incapacidades_' + str(request.user.cliente.id) if request.user.cliente else 'retec_incapacidades_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_tpa': [{"$sortByCount": "$tpa"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vva': [{"$group": {"_id": None, "n": {"$sum": "$vva"}}}],
            'facet_vdo': [{"$group": {"_id": None, "n": {"$sum": "$vdo"}}}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

@login_required(login_url='/login/')
def dashboards(request, section):
    masterId = str(request.user.cliente.id) if request.user.cliente else '0'
    options = ['contratos', 'autorizaciones', 'facturas', 'pagos', 'incapacidades']
    plantilla = 'reservas/dashboards/contratos.html'
    if section in options:
        plantilla = 'reservas/dashboards/' + section + '.html'
    return render(request, plantilla, {'masterId': masterId})

def mng_facet(request):
    coleccion = request.POST.get('tema')
    facets = request.POST.get('facets').split("|")
    matches = [] if request.POST.get('match') == None else request.POST.get('match').split("|")
    limites = [] if request.POST.get('limit') == None else request.POST.get('limit').split("|")
    orden = [] if request.POST.get('sort') == None else request.POST.get('sort').split("|")
    rawper = None if request.POST.get('periodo') == None else int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    # if
    # coleccion += str(request.user.cliente.id) if request.user.cliente else '_0'
    options = {}
    # facets = name:count:field | name:group:field:sum | name:total:field
    #                               0    1     2    3
    for elm in facets:
        tm = elm.split(':')
        if tm[1] == 'count':
            cmp = "$" + tm[2]
            options[tm[0]] = [{"$sortByCount": cmp}]
        elif tm[1] == 'group':
            id = None
            if tm[2].find('-') > 0:
                id = {}
                for fx in tm[2].split('-'):
                    id['tm_' + fx] = "$" + fx
            else:
                id = None if tm[2] == 'none' else "$" + tm[2]
            sum = 1 if len(tm) == 3 or tm[3] == '1' else "$" + tm[3]
            options[tm[0]] = [{"$group": {"_id": id, "total": {"$sum": sum} }}]
            if periodo != None:
                options[tm[0]].insert(0, {"$match": {'crx': periodo}})
    for match in matches:
        #   0       1       2       3
        # facet | field | value | type
        tri = match.split(":")
        if tri[2] == 'exists':
            bool = True if tri[3] == 'true' else False
            if periodo == None:
                options[tri[0]].insert(0, {"$match": {tri[1]: {"$exists": bool}}})
            else:
                options[tri[0]].insert(0, {"$match": {tri[1]: {"$exists": bool}, 'crx': periodo}})
        elif tri[3] == 'int':
            if periodo == None:
                options[tri[0]].insert(0, {"$match": {tri[1]: int(tri[2])}})
            else:
                options[tri[0]].insert(0, {"$match": {tri[1]: int(tri[2]), 'crx': periodo}})
        elif tri[3] == 'str':
            if periodo == None:            
                options[tri[0]].insert(0, {"$match": {tri[1]: str(tri[2])}})
            else:
                options[tri[0]].insert(0, {"$match": {tri[1]: str(tri[2]), 'crx': periodo}})
    for ord in orden:
        aux = ord.split(":")
        options[aux[0]].append({"$sort": {aux[1]: int(aux[2])} })
    for lim in limites:
        lm = lim.split(':')
        options[lm[0]].append({"$limit": int(lm[1])})
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([{"$facet": options}])
    return HttpResponse(datos, content_type="application/json")

def mng_group(request):
    coleccion = request.POST.get('tema')
    action = request.POST.get('action')
    orden = request.POST.get('sort')
    tm = action.split(':')
    options = []
    # group:$campo:$camposum
    if tm[0] == 'count':
        cmp = "$" + tm[1]
        options.append({"$sortByCount": cmp})
    elif tm[0] == 'group':
        id = None if len(tm) == 1 else "$" + tm[1]
        sum = 1 if len(tm) == 2 or tm[2] == '1' else "$" + tm[2]
        options.append({"$group": {"_id": id, "total": {"$sum": sum} }})
    if orden != None:
        aux = orden.split(':')
        options.append({"$sort": {aux[0]: int(aux[1])} })
    mongo = Mongo(coleccion)
    datos = mongo.aggregate(options)
    return HttpResponse(datos, content_type="application/json")

def mng_group_multiple(request):
    coleccion = request.POST.get('tema')
    action = request.POST.get('action')
    tm = action.split(':')
    options = []
    id = {}
    sum = 1 if tm[0] == '1' else "$" + tm[0]
    for cmp in tm[1:]:
        id['tm_' + cmp] = "$" + cmp
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([{"$group": {"_id": id, "total": {"$sum": sum}}}])
    return HttpResponse(datos, content_type="application/json")

def mng_schema(request):
    # mapFun = Code("")
    pass

def mng_distinct(request):
    coleccion = request.POST.get('tema')
    campo = request.POST.get('campo')
    mongo = Mongo(coleccion)
    datos = mongo.distinct(campo)
    return HttpResponse(datos, content_type="application/json")

def mng_view(request):
    coleccion = request.POST.get('tema')
    campo = request.POST.get('campo')
    mongo = Mongo(coleccion)

    print('marquilla ...............')
    # datos = mongo.find({})
    datos = mongo.aggregate([
        {'$match': {}}
    ])
    print(datos)
    return HttpResponse(datos, content_type="application/json")

def mng_fuente_pyr(request):
    fuente = request.POST.get('fuente')
    coleccion = request.POST.get('tema')
    desde = request.POST.get('desde')
    hasta = request.POST.get('hata')
    crx = request.POST.get('crx')
    alias = request.POST.get('consulta')
    clave = request.POST.get('clave')
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id

    consulta = createConsulta(alias, coleccion, clave, cliente_id, user_id)
    etapas = [
        {"$match": {"crx": int(crx)}},
        {"$addFields": {"f_pre": {"$substr": ["$fp", 0, 6]}, "f_rad": {"$substr": ["$fr", 0, 6]}}},
        {"$project": {"f_pre": 1, "f_rad": 1, "vrpbs": 1, "vrpac": 1, "vrpm": 1}},
        {'$facet': {'datos': [
            {"$group": {
                "_id": {"f_pre": "$f_pre", "f_rad": "$f_rad"},
                "total_pbs": {"$sum": "$vrpbs"},
                "total_pac": {"$sum": "$vrpac"},
                "total_pm": {"$sum": "$vrpm"},
            } }
        ]}}
    ]
    if fuente == 'aut':
        etapas = [
            {"$match": {"crx": int(crx)}},
            {"$addFields": {"f_pre": {"$substr": ["$fav", 0, 6]}, "f_rad": {"$substr": ["$fav", 0, 6]}}},
            {"$project": {"f_pre": 1, "f_rad": 1, "vbs": 1, "vac": 1, "vpm": 1}},
            {'$facet': {'datos': [
                {"$group": {
                    "_id": {"f_pre": "$f_pre", "f_rad": "$f_rad"},
                    "total_pbs": {"$sum": "$vbs"},
                    "total_pac": {"$sum": "$vac"},
                    "total_pm": {"$sum": "$vpm"},
                } }
            ]}}
        ]
    if fuente == 'pag':
        etapas = [
            {"$match": {"crx": int(crx)}},
            {"$addFields": {"f_pre": {"$substr": ["$fp", 0, 6]}, "f_rad": {"$substr": ["$fr", 0, 6]}}},
            {"$project": {"f_pre": 1, "f_rad": 1, "vpbs": 1, "vpac": 1, "vppm": 1}},
            {'$facet': {'datos': [
                {"$group": {
                    "_id": {"f_pre": "$f_pre", "f_rad": "$f_rad"},
                    "total_pbs": {"$sum": "$vpbs"},
                    "total_pac": {"$sum": "$vpac"},
                    "total_pm": {"$sum": "$vppm"},
                } }
            ]}}
        ]
    mongo = Mongo(coleccion)
    try:
        datos = mongo.aggregate(etapas)
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        return HttpResponse(datos, content_type="application/json")
        # return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_contratos_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_ctro_dat' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        # 'facet_base': [{"$group": {"_id": "", "base": {"$sum": "$bas"}}}],
        # 'facet_actual': [{"$group": {"_id": "", "actual": {"$sum": "$act"}}}],
        datos = mongo.aggregate([
            {'$match': {'crx': periodo}}, 
            {
                '$facet': {
                    'rs_1': [ {'$group': {'_id': '$pla', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}} ], 
                    'rs_2': [ {'$group': {'_id': '$tpp', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}} ], 
                    'rs_3': [ {'$group': {'_id': '$stt', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}} ], 
                    'rs_4': [ {'$group': {'_id': None, 'suma': {'$sum': '$bas'}}} ], 
                    'rs_5': [ {'$group': {'_id': None, 'suma': {'$sum': '$act'}, 'alldoc': {'$sum': 1} }} ], 
                    'rs_6': [
                        {'$group': {'_id': '$nmp', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}}, 
                        {'$sort': {'suma': -1}}, 
                        {'$limit': 20}
                    ],
                    'rs_7': [ {'$group': {'_id': '$idp', 'total': {'$sum': 1}}} ],
                    'rs_8': [
                        {'$addFields': {'xnum': {"$convert": {"input": "$tar", "to": "string", "onError": "error", "onNull": "null"}} }},
                        {'$group': {'_id': '$xnum', 'total': {'$sum': 1}}} 
                    ]
                }
            }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_auto(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_autorizacion_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_aut_dat' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo} }, 
            {
                '$facet': {
                    'rs_1': [
                        {'$match': {'pmx': {"$in": ['0', 0]}, 'pla': 'S'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vbs'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'rs_2': [
                        {'$match': {'pmx': {"$in": ['0', 0]}, 'pla': 'V'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vbs'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'rs_3': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla': 'S'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpm'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'rs_4': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla': 'V'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpm'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ],
                    'pmx': [{'$group': {'_id': '$pmx', 'total': {'$sum': 1} } }],
                    'facet_amb': [{"$sortByCount": "$amb"}],
                    'facet_pla': [{"$sortByCount": "$pla"}],
                    'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
                    'facet_vbs': [
                        {"$project": {"_id": 0, "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}}}, 
                        {"$group": {"_id": None, "n": {"$sum": "$n_vbs"}}}
                    ],
                    'facet_vac': [{"$group": {"_id": None, "n": {"$sum": "$vac"}}}],
                    'facet_vpm': [
                        {"$project": {"_id": 0, "n_vpm": {"$convert": {"input": "$vpm", "to": "double", "onError": 0, "onNull": 0}}}}, 
                        {"$group": {"_id": None, "n": {"$sum": "$n_vpm"}}}
                    ],
                    'facet_doc': [{"$sortByCount": "$tus"}],
                    'gp_esti': [{'$group': {'_id': '$est', 'total': {'$sum': 1}}}],
                    'gp_stt': [{'$group': {'_id': '$stt', 'total': {'$sum': 1}}}]
                }
            }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_auto_control(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_autorizacion_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_aut_ctr' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {"$project": {'factor': {"$multiply": ["$can", "$vun"]}, 'vbs': 1, 'vpm': 1, 'pmx': 1} },
            {"$group": {'_id': '$pmx', 'sum_fac': {"$sum": "$factor"}, 'sum_vbs': {"$sum": "$vbs"}, 'sum_vpm': {"$sum": "$vpm"} } }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_fac(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_facturas_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    print(tema)
    print(periodo)
    consulta = createConsulta('raw_facet_fac' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    print('hola mundo mongo')
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo} }, 
            {
                '$facet': {
                    'rs_0': [ {'$group': {'_id': '$tus', 'total': {'$sum': 1}}} ], 
                    'rs_1': [ {'$group': {'_id': '$pla', 'total': {'$sum': 1}}} ], 
                    'rs_2': [ {'$group': {'_id': '$tra', 'total': {'$sum': 1}}} ], 
                    'rs_3': [ {'$group': {'_id': '$amb', 'total': {'$sum': 1}}} ], 
                    'rs_4': [ {'$group': {'_id': '$egl', 'total': {'$sum': 1}}} ],
                    'pmx':  [ {'$group': {'_id': '$pmx', 'total': {'$sum': 1}}} ],
                    'gp_ext_01': [{'$group': {'_id': '$tpo', 'total': {'$sum': 1}}}], 
                    'gp_ext_02': [{'$group': {'_id': '$tpp', 'total': {'$sum': 1}}}], 
                    'gp_ext_03': [{'$group': {'_id': '$cov', 'total': {'$sum': 1}}}], 
                    'gp_ext_mec': [{'$group': {'_id': '$mpa', 'total': {'$sum': 1}}}],
                    'cores': [
                        {"$project": {
                            "_id": 0, # sum_vpm
                            "n_vac": {"$convert": {"input": "$vac", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vbs": {"$convert": {"input": "$vrpbs", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vpm": {"$convert": {"input": "$vrpm", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vdo": {"$convert": {"input": "$vdo", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vgl": {"$convert": {"input": "$vgl", "to": "double", "onError": 0, "onNull": 0}},
                            "n_gde": {"$convert": {"input": "$gld", "to": "double", "onError": 0, "onNull": 0}} # $gde
                        }}, 
                        {"$group": {
                            "_id": None, 
                            "total": {"$sum": 1},
                            "sum_vac": {"$sum": "$n_vac"},
                            "sum_vbs": {"$sum": "$n_vbs"}, 
                            "sum_vpm": {"$sum": "$n_vpm"}, 
                            "sum_vdo": {"$sum": "$n_vdo"}, 
                            "sum_vgl": {"$sum": "$n_vgl"}, 
                            "sum_gde": {"$sum": "$n_gde"}
                        }},
                    ],
                    's0': [
                        {"$match": {'pmx': {"$in": ['0', 0]}, 'pla': 'S'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                    'v0': [
                        {"$match": {'pmx': {"$in": ['0', 0]}, 'pla': 'V'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                    's1': [
                        {"$match": {'pmx': {"$in": ['1', 1]}, 'pla': 'S'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                    'v1': [
                        {"$match": {'pmx': {"$in": ['1', 1]}, 'pla': 'V'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                }
            }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_fac_control(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_facturas_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_fac_ctr' + str(rawper), tema, clave, cliente_id, user_id)
    print('vigo: ' + tema)
    mongo = Mongo(tema)
    try:
        # "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {"$addFields": {
                "hg": {"$cond": [{"$in": ["$egl", ["T", "P"]]}, 1, 0]}, # hg has_glosa
                "pmx": {"$convert": {"input": "$pmx", "to": "string", "onError": "", "onNull": ""}},
            }},
            {'$project': {
                'vdo': 1,
                'vpbs': 1,
                'vppm': 1,
                'vgl': 1,
                'gld': 1,
                'vrpbs': 1,
                'vrpm': 1,
                'vdo_0_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vdo", 0]},
                'vdo_0_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vdo", 0]},
                'vgl_0_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vgl", 0]},
                'vgl_0_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vgl", 0]},
                'gld_0_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$gld", 0]},
                'gld_0_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$gld", 0]},
                'vpbs_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vpbs", 0]},
                'vppm_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vppm", 0]},
                'vrpbs_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vrpbs", 0]},
                'vrpm_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vrpm", 0]},
                'vdo_1_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vdo", 0]},
                'vdo_1_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vdo", 0]},
                'vgl_1_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vgl", 0]},
                'vgl_1_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vgl", 0]},
                'gld_1_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$gld", 0]},
                'gld_1_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$gld", 0]},
                'vpbs_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vpbs", 0]},
                'vppm_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vppm", 0]},
                'vrpbs_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vrpbs", 0]},
                'vrpm_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vrpm", 0]},
                'vdo_2_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vdo", 0]},
                'vdo_2_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vdo", 0]},
                'vgl_2_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vgl", 0]},
                'vgl_2_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vgl", 0]},
                'gld_2_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$gld", 0]},
                'gld_2_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$gld", 0]},
                'vpbs_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vpbs", 0]},
                'vppm_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vppm", 0]},
                'vrpbs_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vrpbs", 0]},
                'vrpm_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vrpm", 0]},
            }},
            {'$group': {
                '_id': None,
                's_vdo': {'$sum': '$vdo'},
                's_vpbs': {'$sum': '$vpbs'},
                's_vppm': {'$sum': '$vppm'},
                's_vgl': {'$sum': '$vgl'},
                's_gld': {'$sum': '$gld'},
                's_vrpbs': {'$sum': '$vrpbs'},
                's_vrpm': {'$sum': '$vrpm'},
                's_vdo_0_pbs': {'$sum': '$vdo_0_pbs'},
                's_vdo_0_pm': {'$sum': '$vdo_0_pm'},
                's_vgl_0_pbs': {'$sum': '$vgl_0_pbs'},
                's_vgl_0_pm': {'$sum': '$vgl_0_pm'},
                's_gld_0_pbs': {'$sum': '$gld_0_pbs'},
                's_gld_0_pm': {'$sum': '$gld_0_pm'},
                's_vpbs_0': {'$sum': '$vpbs_0'},
                's_vppm_0': {'$sum': '$vppm_0'},
                's_vrpbs_0': {'$sum': '$vrpbs_0'},
                's_vrpm_0': {'$sum': '$vrpm_0'},
                's_vdo_1_pbs': {'$sum': '$vdo_1_pbs'},
                's_vdo_1_pm': {'$sum': '$vdo_1_pm'},
                's_vgl_1_pbs': {'$sum': '$vgl_1_pbs'},
                's_vgl_1_pm': {'$sum': '$vgl_1_pm'},
                's_gld_1_pbs': {'$sum': '$gld_1_pbs'},
                's_gld_1_pm': {'$sum': '$gld_1_pm'},
                's_vpbs_1': {'$sum': '$vpbs_1'},
                's_vppm_1': {'$sum': '$vppm_1'},
                's_vrpbs_1': {'$sum': '$vrpbs_1'},
                's_vrpm_1': {'$sum': '$vrpm_1'},
                's_vdo_2_pbs': {'$sum': '$vdo_2_pbs'},
                's_vdo_2_pm': {'$sum': '$vdo_2_pm'},
                's_vgl_2_pbs': {'$sum': '$vgl_2_pbs'},
                's_vgl_2_pm': {'$sum': '$vgl_2_pm'},
                's_gld_2_pbs': {'$sum': '$gld_2_pbs'},
                's_gld_2_pm': {'$sum': '$gld_2_pm'},
                's_vpbs_2': {'$sum': '$vpbs_2'},
                's_vppm_2': {'$sum': '$vppm_2'},
                's_vrpbs_2': {'$sum': '$vrpbs_2'},
                's_vrpm_2': {'$sum': '$vrpm_2'},
                'total': {'$sum': 1}
            }}
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_fac_indi(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_facturas_0'
    mongo = Mongo(tema)
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    datos = mongo.aggregate([
        {"$match": {'crx': periodo} },
        {'$group': {
            '_id': None,
            's_vdo': {'$sum': '$vrpbs'},
            's_vpbs': {'$sum': '$vrpm'},
            'total': {'$sum': 1}
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

def raw_facet_pay(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_pagos_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_pay_dat' + str(rawper), tema, clave, cliente_id, user_id)
    print('domora + ' + tema)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo}}, 
            {
                '$facet': {
                    # '$vbs'	'$vpm'
                    'rs_0': [ {'$group': {
                        '_id': None, 
                        'total': {'$sum': 1}, 
                        'sum_vdo': {'$sum': "$vdo"}, 
                        'sum_gde': {"$sum": "$gde"}, 
                        'r_pbs': {'$sum': '$vpbs'}, 
                        'r_pm': {'$sum': '$vppm'} 
                    }}],
                    'rs_1': [ {'$group': {'_id': '$pla', 'total': {'$sum': 1}}} ],
                    'rs_2': [ {'$group': {'_id': '$tra', 'total': {'$sum': 1}}} ],
                    'rs_3': [ {'$group': {'_id': '$amb', 'total': {'$sum': 1}}} ],
                    'rs_4': [ {'$group': {'_id': '$tus', 'total': {'$sum': 1}}} ],
                    'pmx':  [ {'$group': {'_id': '$pmx', 'total': {'$sum': 1}}} ],
                    'new_1': [ {'$group': {'_id': '$tpp', 'total': {'$sum': 1}}} ],
                    'new_2': [ {'$group': {'_id': '$mpa', 'total': {'$sum': 1}}} ],
                    # 'rs_5': [
                    #     {'$match': {'crx': periodo}}, 
                    #     {'$group': {'_id': {'tm_tra': '$tra', 'tm_tus': '$tus'}, 'total': {'$sum': 1}}}
                    # ]
                }
            }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print('dinabot')
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_pay_control(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_pagos_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_pay_ctr' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                's_vdo': {'$sum': '$vdo'},		# FACTURADO TOTAL
                's_gde': {'$sum': '$gde'},		# GLOSA DEFINITIVA
                's_vpbs': {'$sum': '$vpbs'},	# PAGADO PBS
                's_vppm': {'$sum': '$vppm'},	# PAGADO PM
                'f_pbs': {'$sum': {'$cond': [{'$in': ['$pmx', ['0', 0]]}, '$vdo', 0]}},		# FACTURADO PBS
                'f_pm': {'$sum': {'$cond': [{'$in': ['$pmx', ['1', 1]]}, '$vdo', 0]}},		# FACTURADO PM
                'g_pbs': {'$sum': {'$cond': [{'$in': ['$pmx', ['0', 0]]}, '$gde', 0]}},		# GLOSADO PBS
                'g_pm': {'$sum': {'$cond': [{'$in': ['$pmx', ['1', 1]]}, '$gde', 0]}},		# GLOSADO PM
                'total': {'$sum': 1}
            }}
        ])
        # // rawCtr.s_vpbs
        # // rawCtr.s_vppm
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_inca(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_incapacidades_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_inca_dat' + str(rawper), tema, clave, cliente_id, user_id)
    rs0 = {'$group': {'_id': None, 'total': {'$sum': 1}, 'reserva': {'$sum': '$vva'}, 'pagado': {'$sum': '$vdo'}}}
    if tema == 'retec_incapacidades_0':
        rs0 = {'$group': {'_id': None, 'total': {'$sum': 1}, 'reserva': {'$sum': '$vlri'}, 'pagado': {'$sum': '$vlrp'}}}
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo}}, 
            {'$facet': {
                'rs_0': [rs0],
                'rs_1': [{'$group': {'_id': '$tus', 'total': {'$sum': 1}} }],
                'rs_2': [{'$group': {'_id': '$tpa', 'total': {'$sum': 1}} }],
                'tem': [{'$group': {'_id': '$tem', 'total': {'$sum': 1}} }],
                'taf': [{'$group': {'_id': '$taf', 'total': {'$sum': 1}} }],
                'esp': [{'$group': {'_id': '$esp', 'total': {'$sum': 1}} }],
                'tgo': [{'$group': {'_id': '$tgo', 'total': {'$sum': 1}} }],
            }}
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def slice_data(request):
    coleccion = request.POST.get('coleccion')
    campos = request.POST.get('campos')
    pagina = int(request.POST.get('pagina'))
    cantidad = int(request.POST.get('cantidad'))
    salto = cantidad * (pagina - 1)
    project = {cmp:1 for cmp in campos.split(',')}
    project['_id'] = 0
    rawper = int(request.POST.get('periodo'))
    filtros = request.POST.get('filtros')       # field:value | field:value
    periodo = {"$exists": False} if rawper == 0 else rawper
    match = {'crx': periodo}
    print('canton')
    print(coleccion)
    print(salto)
    print(cantidad)
    print(filtros)
    for fil in filtros.split('|'):
        # field : value : bool
        par = fil.split(':')
        if par[1] == 'exists':
            bool = True if par[2] == 'true' else False
            match[par[0]] = {"$exists": bool}
        else:
            match[par[0]] = par[1]
    mongo = Mongo(coleccion)
    print(match)
    datos = mongo.aggregate([
        {'$match': match},
        {'$project': project },
        {'$skip': salto},
        {'$limit': cantidad + 1}
    ])
    print(datos)
    return HttpResponse(datos, content_type="application/json")

def getPeriodos(request):
    # CRX es el nombre del campo destinado para la periodicidad de las bases de datos
    coleccion = request.POST.get('tema')
    # coleccion = "retec_contratos_0"
    print('dayanei')
    print(coleccion)
    mongo = Mongo(coleccion)
    # datos = mongo.aggregate([
    #     {"$match": {"crx": {"$exists": True}}},
    #     {"$group": {"_id": "$crx", "total": {"$sum": 1}}}
    # ])

    # 'unsaved': [{"$match": {"crx": {"$exists": False}}}, {"$count": "total"}],
    datos = mongo.aggregate([
        {"$facet": {
            'saved': [{"$group": {"_id": "$crx", "total": {"$sum": 1}}}],
            # 'saved': [{"$match": {"crx": {"$exists": True}}}, {"$group": {"_id": "$crx", "total": {"$sum": 1}}}],
            # 'sonei': [{"$match": {"crx": {"$exists": False}}}, {"$project": {"created": {"$dateToString": {"format": "%Y-%m-%d", "date": "$_id"}}}}, {"$group": {"_id": "$created", "total": {"$sum": 1}}}]
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

def getCreatedOrphan(request):
    coleccion = request.POST.get('tema')
    coleccion = "retec_contratos_0"
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$match": {"crx": {"$exists": False}}},
        {"$project": {"created": {"$dateToString": {"format": "%Y-%m-%d", "date": "$_id"}}}},
        # {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "_id"}}, "total": {"$sum": 1}}},
        {"$group": {"_id": "$created", "total": {"$sum": 1}}}
    ])
    return HttpResponse(datos, content_type="application/json")

@login_required(login_url='/login/')
def dash_contratos(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'reservas/dashboards/new_contratos.html', {'clienteId': clienteId, 'cliente': cliente})

@login_required(login_url='/login/')
def dash_autorizaciones(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'reservas/dashboards/new_autorizaciones.html', {'clienteId': clienteId, 'cliente': cliente})

@login_required(login_url='/login/')
def dash_facturas(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    indigena = 'off'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
        if request.user.cliente.is_indigena:
            indigena = 'on'
    return render(request, 'reservas/dashboards/new_facturas.html', {'clienteId': clienteId, 'cliente': cliente, 'indigena': indigena})

@login_required(login_url='/login/')
def dash_pagos(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'reservas/dashboards/new_pagos.html', {'clienteId': clienteId, 'cliente': cliente})

@login_required(login_url='/login/')
def dash_incapacidades(request):
    clienteId = '0'
    cliente = 'CAJACOPI'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'reservas/dashboards/new_incapacidades.html', {'clienteId': clienteId, 'cliente': cliente})

def dash_contratos_data(request):
    mongo = Mongo('retec_contratos_0')
    datos = []
    return HttpResponse(datos, content_type="application/json")

def fixedPeriodo(request):
    coleccion = request.POST.get('tema')
    crx = request.POST.get('crx')
    fecha = request.POST.get('fecha')
    periodo = int(request.POST.get('periodo'))
    mongo = Mongo(coleccion)
    if crx != 'void':
        aux = int(crx)
        rs = mongo.updateMany({"crx": aux}, [{"$set": {"crx": periodo}}])
        return HttpResponse(rs, content_type="application/json")
    elif fecha == 'all':
        rs = mongo.updateMany({"crx": {"$exists": False} }, [{"$set": {"crx": periodo}}])
        return HttpResponse(rs, content_type="application/json")
    else:
        # {"$project": {"xfecha": {"$dateToString": {"format": "%Y-%m-%d", "date": "$_id"}}} },
        # {"$match": {"crx": {"$exists": False}, "xfecha": fecha} },
        rs = mongo.updateMany({"crx": {"$exists": False} }, [{"$set": {"crx": periodo}}])
        return HttpResponse(rs, content_type="application/json")

def pyr_data(request):
    d_from = request.POST.get('from')
    d_to = request.POST.get('to')
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_facturas_0'
    mongo = Mongo(tema)
    datos = mongo.aggregate([
        {'$facet': {'datos': [
            {"$project": {"f_pre": {"$substr": ["$fp", 0, 6]}, "f_rad": {"$substr": ["$fr", 0, 6]}, "vdo": 1 } },
            {"$group": {
                "_id": {"f_pre": "$f_pre", "f_rad": "$f_rad"},
                "total": {"$sum": "$vdo"}
            } }
        ]}}
    ])
    return HttpResponse(datos, content_type="application/json")

def schema_factura(request):
    # fields="tpo:tipoObligacion|ifa:idFactura|tpp:tipoIdPrestador|idp:idPrestador|nmp:nombrePrestador|pla:planSalud|tra:TContra|idc:idContrato|tus:tipoIdUsuario|ius:idUsuario|iav:idAvisado|fau:FAuto|amb:Ambito|ids:idServicio|ser:DesServicio|dia:DiagPpal|can:Cant|fp:FPres|fr:FRad|vdo:VlrFacturado|vpbs:VlrPagadoPBS|vpac:VlrPagadoPAC|vppm:VlrPagadoPM|fpa:FPago|mpa:MecPago|egl:EstGlosa|vgl:VlrGlosado|gld:glosaDefinitiva|vrpbs:VlrReservaPBS|vrpac:VlrReservaPAC|vrpm:VlrReservaPM|pmx:pres_Max|pac:PAct|ume:UMed|ffa:FFarma|cov:Covid"
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_facturas_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_factura' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                               #  {$cond: [{$eq: [{$ifNull: ["$vpac", null] }, null] }, 0, 1] } },
                'n_tpo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpo', None] }, None] }, 0, 1] } },
                'n_ifa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ifa', None] }, None] }, 0, 1] } },
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_tra': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tra', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_iav': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iav', None] }, None] }, 0, 1] } },
                'n_fav': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fav', None] }, None] }, 0, 1] } },
                'n_amb': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$amb', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_can': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$can', None] }, None] }, 0, 1] } },
                'n_fp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fp', None] }, None] }, 0, 1] } },
                'n_fr': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fr', None] }, None] }, 0, 1] } },
                'n_vdo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vdo', None] }, None] }, 0, 1] } },
                'n_vpbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpbs', None] }, None] }, 0, 1] } },
                'n_vpac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpac', None] }, None] }, 0, 1] } },
                'n_vppm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vppm', None] }, None] }, 0, 1] } },
                'n_fpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fpa', None] }, None] }, 0, 1] } },
                'n_mpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$mpa', None] }, None] }, 0, 1] } },
                'n_egl': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$egl', None] }, None] }, 0, 1] } },
                'n_vgl': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vgl', None] }, None] }, 0, 1] } },
                'n_gld': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$gld', None] }, None] }, 0, 1] } },
                'n_vrpbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vrpbs', None] }, None] }, 0, 1] } },
                'n_vrpac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vrpac', None] }, None] }, 0, 1] } },
                'n_vrpm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vrpm', None] }, None] }, 0, 1] } },
                'n_pmx': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pmx', None] }, None] }, 0, 1] } },
                'n_pac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pac', None] }, None] }, 0, 1] } },
                'n_ume': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ume', None] }, None] }, 0, 1] } },
                'n_ffa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ffa', None] }, None] }, 0, 1] } },
                'n_cov': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$cov', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def schema_auto(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_autorizacion_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_auto' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        print('iniciando autorization')
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_stt': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$stt', None] }, None] }, 0, 1] } },
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_iav': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iav', None] }, None] }, 0, 1] } },
                'n_fav': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fav', None] }, None] }, 0, 1] } },
                'n_amb': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$amb', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_can': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$can', None] }, None] }, 0, 1] } },
                'n_est': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$est', None] }, None] }, 0, 1] } },
                'n_vun': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vun', None] }, None] }, 0, 1] } },
                'n_vbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vbs', None] }, None] }, 0, 1] } },
                'n_vac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vac', None] }, None] }, 0, 1] } },
                'n_vpm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpm', None] }, None] }, 0, 1] } },
                'n_pmx': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pmx', None] }, None] }, 0, 1] } },
                'n_pac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pac', None] }, None] }, 0, 1] } },
                'n_ume': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ume', None] }, None] }, 0, 1] } },
                'n_ffa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ffa', None] }, None] }, 0, 1] } },
                'n_cov': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$cov', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print('terminated')
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def schema_contrato(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_contratos_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_ctro' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:    
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_stt': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$stt', None] }, None] }, 0, 1] } },
                'n_f1': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f1', None] }, None] }, 0, 1] } },
                'n_f2': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f2', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_tar': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tar', None] }, None] }, 0, 1] } },
                'n_bas': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$bas', None] }, None] }, 0, 1] } },
                'n_act': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$act', None] }, None] }, 0, 1] } },
                'n_f3': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f3', None] }, None] }, 0, 1] } },
                'n_f4': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f4', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def schema_inca(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_incapacidades_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_inca' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:    
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_tem': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tem', None] }, None] }, 0, 1] } },
                'n_iem': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iem', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_taf': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$taf', None] }, None] }, 0, 1] } },
                'n_ipa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ipa', None] }, None] }, 0, 1] } },
                'n_tpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpa', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_cov': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$cov', None] }, None] }, 0, 1] } },
                'n_fip': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fip', None] }, None] }, 0, 1] } },
                'n_ffp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ffp', None] }, None] }, 0, 1] } },
                'n_sal': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$sal', None] }, None] }, 0, 1] } },
                'n_frp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$frp', None] }, None] }, 0, 1] } },
                'n_esp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$esp', None] }, None] }, 0, 1] } },
                'n_fpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fpa', None] }, None] }, 0, 1] } },
                'n_ds': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ds', None] }, None] }, 0, 1] } },
                'n_tgo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tgo', None] }, None] }, 0, 1] } },
                'n_vva': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vva', None] }, None] }, 0, 1] } },
                'n_vdo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vdo', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def schema_pago(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_pagos_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_pay' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    print('Coleccion: ' + tema + ', Periodo: ' + str(rawper))
    try:    
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_ifa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ifa', None] }, None] }, 0, 1] } },
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_tra': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tra', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_iau': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iau', None] }, None] }, 0, 1] } },
                'n_fau': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fau', None] }, None] }, 0, 1] } },
                'n_amb': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$amb', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_can': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$can', None] }, None] }, 0, 1] } },
                'n_fp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fp', None] }, None] }, 0, 1] } },
                'n_fr': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fr', None] }, None] }, 0, 1] } },
                'n_vdo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vdo', None] }, None] }, 0, 1] } },
                'n_gde': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$gde', None] }, None] }, 0, 1] } },
                'n_mpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$mpa', None] }, None] }, 0, 1] } },
                'n_vpbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpbs', None] }, None] }, 0, 1] } },
                'n_vpac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpac', None] }, None] }, 0, 1] } },
                'n_vppm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vppm', None] }, None] }, 0, 1] } },
                'n_fpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fpa', None] }, None] }, 0, 1] } },
                'n_pmx': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pmx', None] }, None] }, 0, 1] } },
                'n_pac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pac', None] }, None] }, 0, 1] } },
                'n_ume': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ume', None] }, None] }, 0, 1] } },
                'n_ffa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ffa', None] }, None] }, 0, 1] } },
                'n_cov': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$cov', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")
