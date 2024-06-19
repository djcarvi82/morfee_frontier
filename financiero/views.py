from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
# from bson.code import Code

# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'financiero/panel_modulo.html')

def search(request):
    return render(request, 'financiero/search.html')

def consulta(request):
    mongo = Mongo("1_finan_public")
    rs = mongo.aggregate([
        {"$facet": {"finanza": [
            {"$project": {'cod': 1, 'den': 1, 'eps': 1, 'val': 1, 'cuenta': {"$substr": ["$cod", 0, 1]}} },
            {"$group": {"_id": {"n_eps": "$eps", "n_cod": "$cuenta"}, "n_den": {"$first": "$den"}, "suma": {"$sum": "$val"} }},
            # {"$sort": {'eps': 1, 'cuenta': 1} },
        ]}}
    ])
    return HttpResponse(rs, content_type="application/json")

def getCuenta(request):
    codigo = str(request.POST.get('codigo'))
    mongo = Mongo("1_finan_cuentas")
    rs = mongo.aggregate([
        {"$match": {'cod': codigo } },
    ])
    return HttpResponse(rs, content_type="application/json")

def getSubcuentas(request):
    pares = {0: 1, 1: 2, 2: 4, 4: 6, 6: 8}
    codigo = str(request.POST.get('codigo')) if request.POST.get('codigo') else ''
    largo = len(codigo)
    largo_next = pares.get(largo)
    match = {'len': largo_next, 'base': codigo } if largo > 0 else {'len': 1}
    mongo = Mongo("1_finan_cuentas")
    rs = mongo.aggregate([
        {"$facet": {"cuentas": [
            {"$project": {'cod': 1, 'den': 1, 'len': 1, 'base': {"$substr": ["$cod", 0, largo]}} },
            {"$match": match },
        ]}}
    ])
    return HttpResponse(rs, content_type="application/json")

def getCuentaSuma(request):
    codigo = str(request.POST.get('codigo'))
    largo = len(codigo)
    mongo = Mongo("1_finan_public")
    rs = mongo.aggregate([
        {"$project": {'cod': 1, 'den': 1, 'eps': 1, 'val': 1, 'base': {"$substr": ["$cod", 0, largo]}} },
        {"$match": {'base': codigo} },
        {"$group": {"_id": {"n_eps": "$eps", "n_cod": "$base"}, "suma": {"$sum": "$val"} }},
    ])
    return HttpResponse(rs, content_type="application/json")

def getTextoSuma(request):
    texto = str(request.POST.get('texto'))
    mongo = Mongo("1_finan_public")
    print(texto)
    rs = mongo.aggregate([
        {"$facet": {
            "datos": [
                {"$match": {'den': {"$regex": texto, "$options": "i"} } },
                {"$group": {"_id": "$eps", "suma": {"$sum": "$val"} } },
            ],
            "codigos": [
                {"$match": {'den': {"$regex": texto, "$options": "i"} } },
                {"$group": {"_id": "$cod", "cuenta": {"$first": "$den"} } },
                {"$sort": {"_id": 1} }
            ]
        }}
    ])
    return HttpResponse(rs, content_type="application/json")


def getEPS(request):
    mongo = Mongo("1_finan_public")
    rs = mongo.aggregate([
        {"$group": {"_id": "$eps"}},
        {"$sort": {"_id": 1}}
    ])
    return HttpResponse(rs, content_type="application/json")
