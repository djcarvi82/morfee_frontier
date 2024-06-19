from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
from . import models
from bson.objectid import ObjectId
import pandas as pd
import json, datetime

@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'aseguramiento/panel_modulo.html')

@login_required(login_url='/login/')
def consulta(request):
    return render(request, 'aseguramiento/consulta.html')

@login_required(login_url='/login/')
def geoLocation(request):
    return render(request, 'aseguramiento/geo_location.html')

def summary(request):
    mongo = Mongo('lma_liquidacion')
    if mongo.isConnect:
        respuesta = mongo.getCliente().aggregate([
            {'$match': {'estado': 'AC'}},
            {'$project': {'_id': 1, 'estado': 1, 'regimen': 1, 'cod_EPS': 1, 'sexo': 1, 'mun': 1, 'zona': 1}},
            {'$facet': {
                'comp1': [{'$sortByCount': '$estado'}],
                'comp2': [{'$sortByCount': '$regimen'}],
                'comp3': [{'$match': {'regimen': 'subsidiado'}}, {'$sortByCount': '$cod_EPS'}],
                'comp4': [{'$match': {'regimen': 'contributivo'}}, {'$sortByCount': '$cod_EPS'}],
                'comp5': [{'$match': {'regimen': 'subsidiado'}}, {'$sortByCount': '$sexo'}],
                'comp6': [{'$match': {'regimen': 'contributivo'}}, {'$sortByCount': '$sexo'}],
                'comp7': [{'$sortByCount': '$mun'}],
                'comp8': [{'$sortByCount': '$zona'}]
                }
            }
        ])
        return HttpResponse(mongo.dumps(respuesta), content_type="application/json")
    else:
        return HttpResponse([], content_type="application/json")

@login_required(login_url='/login/')
def import_list(request):
    return render(request, 'aseguramiento/import_list.html')

def date_to_string(fl):
    if isinstance(fl, datetime.date):
        return fl.isoformat()

def import_history(request):
    lista = []
    if request.user.cliente:
        clid = request.user.cliente.id
        datos  = models.ControlImportAse.objects.filter(cliente_id=clid).values('id', 'tipo', 'periodo', 'estado', 'created_at', 'diccionario')
        lista = list(datos)
        rs = json.dumps(lista, default=date_to_string)
        return HttpResponse(rs, content_type="application/json")
    else:
        datos = models.ControlImportAse.objects.filter(cliente_id__isnull=True).values()
        lista = list(datos)
        rs = json.dumps(lista)
        return HttpResponse(rs, content_type="application/json")

def import_add(request):
    coleccion = 'lma_liq_' + str(request.user.cliente.id) if request.user.cliente else 'lma_liq_0'
    rawFile = request.FILES.get("rawfile")
    imp = models.ControlImportAse()
    imp.tipo = request.POST.get('tipo')
    imp.periodo = request.POST.get('periodo')
    imp.estado = request.POST.get('estado')
    # imp.recurso = rawFile
    imp.cliente = request.user.cliente
    imp.user = request.user
    imp.save()

    # PROCESS MONGODB
    content = pd.read_csv(rawFile, delimiter=",")
    # k = content.columns.values        # NOMBRES DE CABECERAS
    rawcampos = content.columns.values.tolist()
    campos = "|".join(rawcampos)
    content['ctr'] = imp.id
    docs = content.to_dict(orient='records')
    mongo = Mongo(coleccion)
    result = mongo.insertMany(docs)
    if result:
        imp.estado = 2
        imp.diccionario = campos
        imp.save()
        return JsonResponse({'status': 'success', 'pk': imp.id, 'total': len(result.inserted_ids)})
    else:
        imp.delete()
        return JsonResponse({'status': 'failed', 'pk': imp.id, 'total': 0, 'msn': 'Failed insert many in mongodb.'})

def import_delete(request):
    if request.method == "POST":
        id = request.POST.get('codex')
        try:
            target = models.ControlImportAse.objects.get(pk=id)
            coleccion = 'lma_liq_' + str(request.user.cliente.id) if request.user.cliente else 'lma_liq_0'
            mongo = Mongo(coleccion)
            if mongo.removeImport(target.id):
                target.delete()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'msn': 'Falló la eliminación en MongoDB'})
        except models.ControlImportAse.DoesNotExist:
            return JsonResponse({'status': 'failed', 'msn': 'No se encontró la importación referenciada!' + str(id)})

def import_batch(request):
    if request.method == "POST":
        id = int(request.POST.get('codex'))
        pagina = int(request.POST.get('pagina')) if request.POST.get('pagina') else 1
        coleccion = 'lma_liq_' + str(request.user.cliente.id) if request.user.cliente else 'lma_liq_0'
        mongo = Mongo(coleccion)
        total_batch = int(request.POST.get('memory')) if request.POST.get('memory') else mongo.pageCount({'ctr': id})
        datos = mongo.find({'ctr': id}, page=pagina, attach=total_batch)
        return HttpResponse(datos, content_type="application/json")

def import_bdua_con(request):
    coleccion = 'bdua_contributivo_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_contributivo_0'
    return render(request, 'aseguramiento/contributivo/cont_import.html', {'coleccion': coleccion})


# **************************************************************
# ******************** SECTION CONTRIBUTIVO ********************
# **************************************************************
@login_required(login_url='/login/')
def cont_panel(request, section):
    if section == 'inicio':
        return cont_inicio(request)
    elif section == 'table':
        return cont_table(request)
    elif section == 'import':
        return cont_import(request)
    # return render(request, 'aseguramiento/contributivo/cont_inicio.html')

def cont_inicio(request):
    return render(request, 'aseguramiento/contributivo/cont_inicio.html')

def cont_import(request):
    coleccion = 'bdua_contributivo_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_contributivo_0'
    return render(request, 'aseguramiento/contributivo/cont_import.html', {'coleccion': coleccion})

def cont_table(request):
    coleccion = 'bdua_contributivo_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_contributivo_0'
    return render(request, 'aseguramiento/contributivo/cont_table.html', {'coleccion': coleccion})

def cont_dash(request):
    coleccion = 'bdua_contributivo_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_contributivo_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_tp': [{"$sortByCount": "$tp"}],
            'facet_eps': [{"$sortByCount": "$eps"}],
            'facet_sexo': [{"$sortByCount": "$x1"}],
            'facet_mcpio': [{"$project": {"depmun": {"$concat": ["$dp", "$mc"]}}}, {"$group": {"_id": "$depmun", "total": {"$sum": 1}}}],
            # {"$group": {"_id": "$depmun", "total": {"$sum": 1}}}
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


# **************************************************************
# ******************** SECTION SUBSIDIADO **********************
# **************************************************************
@login_required(login_url='/login/')
def sub_panel(request, section):
    if section == 'inicio':
        return sub_inicio(request)
    elif section == 'table':
        return sub_table(request)
    elif section == 'import':
        return sub_import(request)

def sub_inicio(request):
    return render(request, 'aseguramiento/subsidiado/sub_inicio.html')

def sub_import(request):
    coleccion = 'bdua_subsidiado_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_subsidiado_0'
    return render(request, 'aseguramiento/subsidiado/sub_import.html', {'coleccion': coleccion})

def sub_table(request):
    coleccion = 'bdua_subsidiado_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_subsidiado_0'
    return render(request, 'aseguramiento/subsidiado/sub_table.html', {'coleccion': coleccion})

def sub_dash(request):
    coleccion = 'bdua_subsidiado_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_subsidiado_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_zona': [{"$sortByCount": "$zn"}],
            'facet_eps': [{"$sortByCount": "$eps"}],
            'facet_tipo': [{"$sortByCount": "$x13"}],
            'facet_mcpio': [{"$project": {"depmun": {"$concat": ["$dp", "$mc"]}}}, {"$group": {"_id": "$depmun", "total": {"$sum": 1}}}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


# **********************************************************
# ******************** SECTION SISBÉN **********************
# **********************************************************
@login_required(login_url='/login/')
def sisben_panel(request, section):
    if section == 'inicio':
        return sisben_inicio(request)
    elif section == 'table':
        return sisben_table(request)
    elif section == 'import':
        return sisben_import(request)

def sisben_inicio(request):
    return render(request, 'aseguramiento/sisben/sisben_inicio.html')

def sisben_import(request):
    coleccion = 'bdua_sisben_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_sisben_0'
    return render(request, 'aseguramiento/sisben/sisben_import.html', {'coleccion': coleccion})

def sisben_table(request):
    coleccion = 'bdua_sisben_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_sisben_0'
    return render(request, 'aseguramiento/sisben/sisben_table.html', {'coleccion': coleccion})

def sisben_dash(request):
    coleccion = 'bdua_sisben_' + str(request.user.cliente.id) if request.user.cliente else 'bdua_sisben_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_zona': [{"$sortByCount": "$ZONA"}],
            'facet_depto': [{"$sortByCount": "$DEPTO"}],
            'facet_sexo': [{"$sortByCount": "$SEXO"}],
            'facet_nivel': [{"$sortByCount": "$NIVEL"}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


# *******************************************************
# ******************** SECTION LMA **********************
# *******************************************************
@login_required(login_url='/login/')
def lma_panel(request, section):
    if section == 'inicio':
        return lma_inicio(request)
    elif section == 'import':
        return lma_import(request)

def lma_inicio(request):
    return render(request, 'aseguramiento/lma/lma_inicio.html')

def lma_import(request):
    coleccion = 'lma_liq_' + str(request.user.cliente.id) if request.user.cliente else 'lma_liq_0'
    return render(request, 'aseguramiento/lma/lma_import.html', {'coleccion': coleccion})



def temo(request):
    if request.method == "POST":
        rawFile = request.FILES.get('rawfile')
        contenido = pd.read_csv(rawFile, delimiter=",")
        k = contenido.columns.values        # NOMBRES DE CABECERAS
        contenido['codex'] = 'miyagi'
        docs = contenido.to_dict(orient='records')
        mongo = Mongo('tmp_practice')
        try:
            rs = mongo.insertMany(docs)
            print('todo bien')
        except:
            print('todo mal')
    return render(request, 'aseguramiento/temo.html')

def getGeodata(request):
    # mod = request.POST.get('modulo')
    # rs = Diccionario.objects.filter(modulo=mod, cliente_id__isnull=True).values('id', 'modulo', 'alias', 'coleccion', 'cliente_id') if keyref == 0 else Diccionario.objects.filter(modulo=mod, cliente_id=keyref).values('id', 'modulo', 'alias', 'coleccion', 'cliente_id')
    # data = list(rs)
    # coleccion = 'red_nativa_' + str(request.user.cliente.id) if request.user.cliente else 'red_nativa_0'
    dep = request.POST.get('depto')
    mcp = request.POST.get('mcpio')
    pre = request.POST.get('prestador')
    nat = request.POST.get('natu')
    servi = request.POST.get('servi')
    cups = request.POST.get('cups').split('|') if request.POST.get('cups') != '' else []
    filtros = {}
    if dep != '' : filtros['dep'] = dep
    if mcp != '' : filtros['mcp'] = mcp
    if pre != '' : filtros['nom'] = {"$regex": pre, "$options": "i"}
    if nat != '' : filtros['nat'] = nat
    if servi != '' : filtros['servicios.cod'] = servi
    if len(cups) > 0: filtros['cups.CODIGO'] = {"$in": cups}
    mongo = Mongo('red_nativa_1')
    data = mongo.find(filtros, pro={"cups": 0, "rep": 0, "rso": 0, "sed": 0, "servicios": 0})
    # loc, nom, dep, mcp, dir, nat    
    # data = [{'lat': 8.750282, 'lng': -75.880082}, {'lat': 8.750282, 'lng': -75.380082}, {'lat': 8.750282, 'lng': -75.180082}]
    return HttpResponse(data, content_type="application/json")
    # return JsonResponse(data, safe=False)

def getGeodataId(request):
    id = request.POST.get('id')
    mongo = Mongo('red_nativa_1')
    data = mongo.findOne({"_id": ObjectId(id)})
    return HttpResponse(data, content_type="application/json")

def getProximity(request):
    lat = float(request.POST.get('lat'))
    lng = float(request.POST.get('lng'))
    limite = int(request.POST.get('limite'))
    nat = request.POST.get('natu')
    servi = request.POST.get('servi')
    cups = request.POST.get('cups').split('|') if request.POST.get('cups') != '' else []
    campos = {"dep": 1, "dir": 1, "ema": 1, "loc": 1, "mcp": 1, "nat": 1, "nit": 1, "nom": 1, "tel": 1}
    campos['dist'] = {"$sum": [{"$abs": {"$sum": [lat, {"$multiply": [{"$arrayElemAt": ['$loc', 0]}, -1] }]} }, {"$abs": {"$sum": [lng, {"$multiply": [{"$arrayElemAt": ['$loc', 1]}, -1] }]} }]}
    match = {}
    if nat != '' : match['nat'] = nat
    if servi != '' : match['servicios.cod'] = servi
    if len(cups) > 0: match['cups.CODIGO'] = {"$in": cups}


    options = [{"$match": match}] if match else []
    options.append({"$project": campos})
    options.append({"$sort": {"dist": 1}})
    if limite != None and limite > 0:
        options.append({"$limit": limite})
    print(options)
    mongo = Mongo('red_nativa_1')
    datos = mongo.aggregate(options)
    return HttpResponse(datos, content_type="application/json")

def getGrupo(request):
    coleccion = request.POST.get('coleccion')   # 'red_nativa_1'
    grupos = request.POST.get('grupo').split(':')
    isCount = True if request.POST.get('sumar') != None else False
    items = "$" + grupos[0] if len(grupos) == 1 else dict([(elm, "$"+elm) for elm in grupos])
    query = {"_id": items}
    if isCount: query['total'] = {"$sum": 1}
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'rs': [{"$group": query}]
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

@login_required(login_url='/login/')
def tpl_geocode(request):
    return render(request, 'aseguramiento/geocode.html')

@login_required(login_url='/login/')
def tpl_manager_geo(request):
    return render(request, 'aseguramiento/manager_geocode.html')

def getRedNativa(request):
    # stages.append({"$match": filtro })
    # stages.append({"$project": {"numero_radicacion":1, "razon_social":1, "factura":1, "fecha_radicado":1, "usuario_auditoria_tecnica":1, "estado_tecnica":1}})
    # stages.append({'$skip': salto})
    # stages.append({'$limit': cantidad + 1})
    mongo = Mongo('red_nativa_1')
    datos = mongo.aggregate([
        {'$facet': {
            'prestadores': [
                {"$match": {"hab": {"$exists": True}} },
                {"$project": {"rso": 1, "dep": 1, "mcp": 1, "dir": 1, "hab": 1, "loc": 1} }
            ],
            'kalima': [
                {"$addFields": {"lat": {"$arrayElemAt": ["$loc", 0]}, "lng": {"$arrayElemAt": ["$loc", 1]} } },
                # {"$addFields": {"sincor": {'$cond': [{"$or": [{"loc.0": None}, {"loc.1": None}]}, 'no', 'yes']} } },
                # {"$match": {"$or": [{"loc.0": None}, {"loc.1": None}]} },
                {"$project": {"sincor": {"$or": ["$lat", "$lng"]}, "lat": 1, "lng": 1, "rso": 1, "dep": 1, "mcp": 1, "dir": 1, "hab": 1, "loc": 1} },
                # {"$project": {"lat": 1, "lng": 1, "rso": 1, "dep": 1, "mcp": 1, "dir": 1, "hab": 1, "loc": 1} },
                {"$group": {"_id": "$sincor", "total": {"$sum": 1} } }
            ]
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def saveCoord(request):
    id = request.POST.get('id')
    lat = float(request.POST.get('lat')) if request.POST.get('lat') else None
    lng = float(request.POST.get('lng')) if request.POST.get('lng') else None
    address = request.POST.get('dir')
    cambio = {"loc": [lat, lng]}
    if address:
        cambio.setdefault('dir', address)
    mongo = Mongo('red_nativa_1')
    # data = mongo.updateOne({"_id": ObjectId(id)}, )
    rs = mongo.updateOne({"_id": ObjectId(id)}, cambio, False)
    status = 'success' if rs else 'failed'
    return JsonResponse({'status': status, 'ref': id, 'msn': 'Welcome to morfee!'})

