from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
from datetime import datetime

# Create your views here.
@login_required(login_url='/login/')
def template_inicio(request):
    return render(request, 'ghg/panel_modulo.html')

@login_required(login_url='/login/')
def template_kardex(request):
    return render(request, 'ghg/kardex.html')

@login_required(login_url='/login/')
def template_import(request):
    return render(request, 'ghg/import.html')

def dataini(request):
    vigencia = int(request.POST.get('vigencia')) if request.POST.get('vigencia') else datetime.now().year
    mes = int(request.POST.get('mes')) if request.POST.get('mes') else 0
    filtro = {"y": vigencia}
    facet = {}
    if mes > 0:
        filtro['m'] = mes
    f_tmed = request.POST.get('f_tmed')
    f_tpo = request.POST.get('f_tpo')
    f_tm = request.POST.get('f_tm')
    f_code = request.POST.get('f_code')
    f_point = request.POST.get('f_point')
    f_pro = request.POST.get('f_pro')
    if f_tmed:
        # {'$match': {'pmx': {"$in": ['0', 0]}, 'pla': 'S'}}, 
        filtro['tmed'] = "" if f_tmed == '-empty-' else {"$in": [int(f_tmed), str(f_tmed)]}
    if f_tpo:
        filtro['tpo'] = "" if f_tpo == '-empty-' else {"$in": [int(f_tpo), str(f_tpo)]}
    if f_tm:
        filtro['tm'] = {"$in": [int(f_tm), str(f_tm)]}
    if f_code:
        if f_point == 'code':
            filtro['cm'] = {"$in": [int(f_code), str(f_code)]}
        else:
            filtro['gn'] = {"$regex": f_code, "$options": "i"}
    if f_pro:
        filtro['pro'] = "" if f_pro == '-empty-' else f_pro
    print(filtro)
    mongo = Mongo('ghg_compras')
    datos = mongo.aggregate([
        {"$addFields": {
            "derr": {"$toDate": "1900-01-01"}, 
            "ncan": {"$convert": {"input": "$can", "to": "int", "onError": 0, "onNull": 0}}, 
            "nvun": {"$convert": {"input": "$vun", "to": "int", "onError": 0, "onNull": 0}}
        }},
        {"$addFields": {"raw": {"$convert": {"input": "$f_c", "to": "date", "onError": "$derr", "onNull": "$derr"}} }},
        {"$addFields": {
            'y': {"$year": "$raw"}, 
            'm': {"$month": "$raw"}, 
            'd': {"$dayOfMonth": "$raw"}, 
            'cavun': {"$multiply": ["$ncan", "$nvun"]}
        }},
        {"$match": filtro },
        {"$facet": {
            # 'anios':  [{"$group": {"_id": "$y"} }, {"$sort": {"_id": 1}} ],
            'periodos': [
                {"$group": {"_id": "$m", "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } },
                {"$sort": {"_id": 1}}
            ],
            'tipos': [
                {"$group": {"_id": "$tpo", "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } },
                {"$sort": {"_id": 1}}
            ],
            'moves': [
                {"$group": {"_id": "$tm", "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } }
            ],
            'timedis': [
                {"$group": {"_id": "$tmed", "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } },
                {"$sort": {"_id": 1}}
            ],
            'codmed': [
                # {"$group": {"_id": "$cm", "cmx": {"$first": "$gn"}, "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } }
                {"$group": {"_id": {"xa": "$cm", "xb": "$nvun"}, "cmx": {"$first": "$gn"}, "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } },
                {"$sort": {"cmx": 1} }
            ],
            'providers': [
                {"$group": {"_id": "$pro", "suma": {"$sum": "$cavun"}, "total": {"$sum": "$ncan"}, "lines": {"$sum": 1} } },
                {"$sort": {"suma": -1}},
                # {"$limit": 15}
            ],
            'cnt_cantidad': [
                {"$group": {"_id": None, "suma": {"$sum": "$ncan"} } }
            ],
            'cnt_costo': [
                {"$group": {"_id": None, "suma": {"$sum": "$cavun"} } }
            ],
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

# Pending for delete ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
def kpi_control(request):
    vigencia = request.POST.get('vigencia')
    mes = request.POST.get('mes')
    dia = int(request.POST.get('dia')) if request.POST.get('dia') else 0
    filtro = {'anio': int(vigencia), 'mes': int(mes)}
    auditor = request.POST.get('f_auditor')
    estado = request.POST.get('f_estado')
    conci = request.POST.get('f_conci')
    if dia > 0:
        filtro['dia'] = {'$lte': dia}
    if auditor:
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-empty-' else auditor
    if estado:
        filtro['estado_tecnica'] = "" if estado == '-empty-' else estado
    if conci:
        filtro['formi'] = conci
    print(filtro)
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$addFields": {"derr": {"$toDate": "1900-01-01"}, 'tsum': {"$sum":['$valor_total_acepta_eps', '$valor_total_acepta_ips']} }},
        {"$addFields": {"raw": {"$convert": {"input": "$fecha_radicado", "to": "date", "onError": "$derr", "onNull": "$derr"}} }},
        # {"$project":   {'anio': {"$year": "$raw"}, 'mes': {"$month": "$raw"}, 'dia': {"$dayOfMonth": "$raw"}, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, "fecha_radicado": 1, 'valor_factura': 1, 'total_glosas': 1, 'total_glosa': 1, 'total_pagar': 1, 'razon_social': 1, 'tsum': 1, "formi":{'$cond': [{'$eq': ['$tsum', '$total_glosa'] }, 'equal', 'diff']} }},
        {"$addFields": {'anio': {"$year": "$raw"}, 'mes': {"$month": "$raw"}, 'dia': {"$dayOfMonth": "$raw"}, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, "formi":{'$cond': [{'$eq': ['$tsum', '$total_glosa'] }, 'Conciliado', 'Sin conciliar']} }},
        {"$match": filtro },
        {'$facet': {
            'periodo': [
                {"$group": {"_id": "$formi", "total": {"$sum": 1}, "sglo": {"$sum": "$total_glosa"}, "seip": {"$sum": "$tsum"} }},
            ],
            'estado': [
                {"$group": {"_id": "$estado_tecnica", "total": {"$sum": 1} }},
            ],
            'auditor': [
                {"$group": {"_id": "$usuario_auditoria_tecnica", "total": {"$sum": 1} }},
            ],
            'fechas': [
                {"$group": {"_id": "$fecha_radicado", "total": {"$sum": 1} }},
                {"$sort": {"_id": 1}}
            ],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")



