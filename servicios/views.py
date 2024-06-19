from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
from datetime import date

# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'servicios/panel_modulo.html')

@login_required(login_url='/login/')
def hc_show(request):
    return render(request, 'servicios/hc_show.html')

@login_required(login_url='/login/')
def hc_register(request):
    return render(request, 'servicios/hc_register.html')

def hc_search_doc(request):
    tdoc = request.POST.get('tdoc')
    ndoc = request.POST.get('ndoc')
    mongo = Mongo('serv_usuarios')
    user = mongo.findOne({'tdoc': tdoc, 'ndoc': ndoc})
    return HttpResponse(user, content_type="application/json")

def hc_search_consulta(request):
    tdoc = str(request.POST.get('tdoc'))
    ndoc = str(request.POST.get('ndoc'))
    mongo = Mongo('serv_consultas')
    datos = mongo.aggregate([
        {"$match": {'tdoc': tdoc, 'ndoc': ndoc} },
        {"$sort": {"fec": -1} },
        {"$limit": 2}
    ])
    return HttpResponse(datos, content_type="application/json")

def hc_save_doc(request):
    has_user = request.POST.get('has_user')
    if has_user == 'no':
        cmp = ['tdoc','ndoc','n1','n2','a1','a2','fnac','sex','eci','dir','tel','dep','mcp','reg','niv','ocu','eps','tvin','aco','aco_tel','res','res_tel','res_par']
        userdata = {}
        for elm in cmp:
            userdata[elm] = str(request.POST.get(elm))
        mini = Mongo('serv_usuarios')
        yum = mini.insertOne(userdata)
    csf = ['fec', 'tser', 'tcon', 'nota', 'cup', 'fin', 'cau', 'tdiag', 'diag', 'diag_tx', 'med', 'area', 'nreg']
    consulta = {}
    consulta['tdoc'] = str(request.POST.get('tdoc'))
    consulta['ndoc'] = str(request.POST.get('ndoc'))
    for cm in csf:
        consulta[cm] = str(request.POST.get(cm))
    mongo = Mongo('serv_consultas')
    rs = mongo.insertOne(consulta)
    return HttpResponse({'status': 'success'}, content_type="application/json")



