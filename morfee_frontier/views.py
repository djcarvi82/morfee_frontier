from dataclasses import fields
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.template.defaulttags import register
from django.http import HttpResponse, JsonResponse
from users.models import AuthModulo, AuthCliente, Diccionario
from . import forms
import json
# from bson.objectid import ObjectId

@register.filter
def get_modulo(lista, clave):
    try:
        lista.index(clave)
        return True
    except ValueError:
        return False

@login_required(login_url='/login/')
def inicio(request):
    modulos = AuthModulo.objects.all()
    # lista = {'ase': True, 'sp': True}
    return render(request, 'morfee_frontier/inicio.html', {'modulos': modulos, 'cantidad': len(modulos)})

@login_required(login_url='/login/')
def diccionario(request):
    return render(request, 'morfee_frontier/diccionario.html')

def sin_pagina(request, exception):
    return render(request, '404.html', status=404)

class CustomLoginView(LoginView):
    authentication_form = forms.CustomAuthenticationForm

class CustomChangePWDView(PasswordChangeView):
    form_class = forms.CustomPasswordChangeForm

def logout_view(request):
    logout(request)
    return redirect('login')

def infoForDictio(request):
    cli = AuthCliente.objects.all().values('id', 'cliente')
    mods = AuthModulo.objects.all().values('id', 'modulo', 'clave')
    return JsonResponse({'result': {'clientes': list(cli), 'modulos': list(mods)}})

def getCollections(request):
    cliente_id = request.POST.get('cliente_id')
    mod = request.POST.get('modulo')
    rs = Diccionario.objects.filter(modulo=mod, cliente_id=cliente_id).values('id', 'modulo', 'alias', 'coleccion', 'cliente_id') if cliente_id != None else Diccionario.objects.filter(modulo=mod, cliente_id__isnull=True).values('id', 'modulo', 'alias', 'coleccion', 'cliente_id')
    data = list(rs)
    return JsonResponse(data, safe=False)

def getCollection(request):
    id = request.POST.get('id')
    data = Diccionario.objects.get(pk=id)
    rs = {'id': data.id, 'modulo': data.modulo, 'alias': data.alias, 'coleccion': data.coleccion, 'cliente_id': data.cliente_id, 'campos': data.campos, 'reglas': data.reglas, 'type_head': data.type_head}
    return JsonResponse(rs)

def updateField(request):
    dic_id = request.POST.get('dic_id')
    fieldname = request.POST.get('fieldname')
    fieldvalue = request.POST.get('fieldvalue')
    try:
        dictio = Diccionario.objects.get(pk=dic_id)
        setattr(dictio, fieldname, fieldvalue)
        dictio.save()
        rs = {'status': 'success', 'id': dictio.id, 'modulo': dictio.modulo, 'alias': dictio.alias, 'coleccion': dictio.coleccion, 'cliente_id': dictio.cliente_id, 'campos': dictio.campos, 'reglas': dictio.reglas, 'type_head': dictio.type_head}
        return JsonResponse(rs)
    except Diccionario.DoesNotExist:
        return JsonResponse({'status': 'failed'})

def dicsOfUser(request):
    keyref = int(request.POST.get('keyref'))
    mod = request.POST.get('modulo')
    rs = Diccionario.objects.filter(modulo=mod, cliente_id__isnull=True).values('id', 'modulo', 'alias', 'coleccion', 'cliente_id') if keyref == 0 else Diccionario.objects.filter(modulo=mod, cliente_id=keyref).values('id', 'modulo', 'alias', 'coleccion', 'cliente_id')
    data = list(rs)
    return JsonResponse(data, safe=False)
