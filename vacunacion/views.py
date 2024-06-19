from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
from bson.objectid import ObjectId
from vacunacion import forms
import json

@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'vacunacion/inicio.html')

@login_required(login_url='/login/')
def busqueda(request):
    return render(request, 'vacunacion/busqueda.html')

def jxSearchIndividual(request):
    criterio = request.GET.get('criterio')
    params = {}
    opt = ['t_doc', 'n_doc', 'bdua'] if criterio == 'ident' else ['nom_1', 'nom_2', 'ape_1', 'ape_2']
    specials = ['nom_1', 'nom_2', 'ape_1', 'ape_2']
    for op in opt:
        if request.GET.get(op) != None:
            if op in specials:
                params[op] = {"$regex": request.GET.get(op), "$options": "i"}
            else:
                params[op] = request.GET.get(op)
    mongo = Mongo("vacunacion")
    print('Params here!')
    print(params)
    datos = mongo.find(params, 1, 11, pro={'nom_1': 1, 'nom_2': 1, 'ape_1': 1, 'ape_2': 1, 't_doc': 1, 'n_doc': 1, 'edad': 1, 'estado': 1, 'dep': 1,  'mun': 1, 'mun_res': 1, 'cod_EPS': 1, 'dane': 1, 'sisben': 1, 'paiweb': 1, 'lat': 1, 'lng': 1})
    return HttpResponse(datos, content_type="application/json")

def agendar(request, id):
    modulo = 'app_vac'
    if ObjectId.is_valid(id) == False:
        return render(request, 'anexos/not_found.html', {'modulo': modulo, 'mensaje': 'El id ' + id + ' no es válido.'})
    mongo = Mongo('vacunacion')
    rl = mongo.findOne({'_id': ObjectId(id)})
    dato = json.loads(rl)
    # rl = Vacunacion.objects.get(pk=ObjectId(id))
    if request.method == "POST":
        form = forms.AgendaForm(request.POST)
        if form.is_valid():
            cita = {'_id': ObjectId(), 'g_r': request.POST.get('g_r'), 'g_o': request.POST.get('g_o'), 'l_p': request.POST.get('l_p'), 't_f': request.POST.get('t_f'), 't_h': request.POST.get('t_h')}
            mongo.updateOne({"_id": ObjectId(id)}, {"agenda": cita})
            return redirect('vac_agendar', id)
        else:
            return render(request, 'vacunacion/agendar.html', {'modulo': modulo, 'dato': rl, 'form': form})
    else:
        return render(request, 'vacunacion/agendar.html', {'modulo': modulo, 'dato': dato, 'form': forms.AgendaForm()})
    # else:
    #     return render(request, 'anexos/not_found.html', {'modulo': modulo, 'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})
