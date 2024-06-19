from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
from bson.objectid import ObjectId
import json
import qrcode
import base64
import io
# import pyodbc
from django.core.files.storage import FileSystemStorage
from . import models


# from django.conf import settings
# import pandas as pd
# import os
# from pymongo import MongoClient

# from morfee_frontier.settings import CUSTOM_URI_MONGO, CUSTOM_DB_MONGO

# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'auditorias/inicio.html')

@login_required(login_url='/login/')
def prueba_s3(request):
    if request.method == 'POST':
        recurso = request.FILES['archivo']
        ruta = ''
        try :
            upload = models.Upload(file=recurso)
            upload.save()
            ruta = upload.file.url
            print('Url ▼')
            print(upload.file.url)
            print('Path ▼')
            print(upload.file.path)

            return render(request, 'auditorias/pooja/prueba_s3.html', {'ruta': ruta, 'estado': 'success'})
        except :
            return render(request, 'auditorias/pooja/prueba_s3.html', {'ruta': ruta, 'estado': 'failed'})
    return render(request, 'auditorias/pooja/prueba_s3.html', {'ruta': '', 'estado': '--'})

@login_required(login_url='/login/')
def facturacion(request):
    return render(request, 'auditorias/facturacion.html')

@login_required(login_url='/login/')
def glosaTemplate(request):
    return render(request, 'auditorias/glosa.html')

@login_required(login_url='/login/')
def estadoTemplate(request):
    return render(request, 'auditorias/estado.html')

@login_required(login_url='/login/')
def importea(request):
    return render(request, 'auditorias/import.html')

@login_required(login_url='/login/')
def import_glosa(request):
    return render(request, 'auditorias/import_glosa.html')

@login_required(login_url='/login/')
def import_us(request):
    return render(request, 'auditorias/import_rips_us.html')

@login_required(login_url='/login/')
def import_ac(request):
    return render(request, 'auditorias/import_rips_ac.html')

@login_required(login_url='/login/')
def import_ap(request):
    return render(request, 'auditorias/import_rips_ap.html')

@login_required(login_url='/login/')
def import_af(request):
    return render(request, 'auditorias/import_rips_af.html')

@login_required(login_url='/login/')
def import_ah(request):
    return render(request, 'auditorias/import_rips_ah.html')

@login_required(login_url='/login/')
def import_am(request):
    return render(request, 'auditorias/import_rips_am.html')

@login_required(login_url='/login/')
def import_at(request):
    return render(request, 'auditorias/import_rips_at.html')

@login_required(login_url='/login/')
def import_au(request):
    return render(request, 'auditorias/import_rips_au.html')


@login_required(login_url='/login/')
def importAlt(request):
    return render(request, 'auditorias/import_alt.html')

@login_required(login_url='/login/')
def kpi(request):
    return render(request, 'auditorias/kpi.html')

@login_required(login_url='/login/')
def resumen(request):
    return render(request, 'auditorias/resumen.html')

@login_required(login_url='/login/')
def consulta(request):
    return render(request, 'auditorias/consulta.html')

@login_required(login_url='/login/')
def general(request):
    return render(request, 'auditorias/general.html')

def getGeneralVue(request):
    mongo = Mongo("audit_facturas_0")
    datos = mongo.aggregate([
        {"$facet": {
            'facet_sum': [
                {"$project": {"vigencia_f_inicial": 1, "vigencia_f_final": 1, "numero_contrato": 1, "nit": 1, "factura": 1, "razon_social": 1, "valor_contrato": 1, "codigo_prestador": 1, "digito_verificacion": 1, "alt_neto": {"$toLong": "$valor_neto"}, "alt_copago": {"$toLong": "$valor_total_copago"}, "alt_rete": {"$toLong": "$total_retefuente"}, "alt_iva": {"$toLong": "$total_reteiva"}, "alt_pay": {"$toLong": "$total_pagar"}}},
                {"$group": {"_id": {"n_nit": "$nit", "n_ref": "$numero_contrato"}, "vige_ini": {"$first": "$vigencia_f_inicial"}, "vige_fin": {"$first": "$vigencia_f_final"}, "val_contrato": {"$first": "$valor_contrato"}, "razon": {"$first": "$razon_social"}, "codpre": {"$first": "$codigo_prestador"}, "digito": {"$first": "$digito_verificacion"}, "sum_neto": {"$sum": "$alt_neto"}, "sum_copago": {"$sum": "$alt_copago"}, "sum_rete": {"$sum": "$alt_rete"}, "sum_iva": {"$sum": "$alt_iva"}, "sum_pay": {"$sum": "$alt_pay"}, "count_fac": {"$sum": 1} }},
                {"$sort": {"val_contrato": 1}}
            ],
            'facet_con': [
                {"$group": {"_id": "$tipo_contrato", "total": {"$sum": 1}} }
            ],
            'facet_mod': [
                {"$group": {"_id": "$modalidad_contrato", "total": {"$sum": 1}} }
            ],
            'facet_reg': [
                {"$group": {"_id": "$tipo_regimen", "total": {"$sum": 1}} }
            ],
            'facet_pos': [
                {"$group": {"_id": "$pos", "total": {"$sum": 1}} }
            ],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def getFacturasVue(request):
    nit = request.POST.get('nit')
    ref = request.POST.get('contrato')
    mongo = Mongo("audit_facturas_0")
    datos = mongo.aggregate([
        # filtro['nit'] = {"$in": [str(nit), int(nit)]}
        {"$match": {"numero_contrato": ref, "nit": {"$in": [int(nit), str(nit)]} } },
        {"$project": {"numero_contrato": 1, "factura": 1, "fecha_radicado": 1, "usuario_auditoria_tecnica": 1, "valor_neto": 1, "valor_total_copago": 1, "total_retefuente": 1, "total_reteiva": 1, "tipo_regimen": 1, "pos": 1, "usuario_radica": 1}},
    ])
    return HttpResponse(datos, content_type="application/json")

def getDetailsVue(request):
    ref = request.POST.get('contrato')
    mongo = Mongo("audit_rip_af_0")
    print({"$match": {"nco": str(ref) } })
    datos = mongo.aggregate([
        {"$facet": {
            'facet_fac': [
                {"$match": {"nco": str(ref) } }
            ],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def getFacturasXFecha(request):
    nit = request.POST.get('nit')
    periodo = request.POST.get('periodo')
    user = request.POST.get('user')
    filtro = {}
    aux = False
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
        aux = True
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
        aux = True
    if user != "":
        kuser = "" if user == '(Vacio)' else user
        filtro['usuario_auditoria_tecnica'] = kuser
        aux = True

    stages = []
    if aux:
        stages.append({"$match": filtro })
    stages.append({"$project": {"fecha_radicado": 1} })
    stages.append({"$group": {"_id": "$fecha_radicado", "total": {"$sum": 1}} })
    stages.append({"$sort": {"_id": 1}})
    print(stages)
    mongo = Mongo("audit_facturas_0")
    datos = mongo.aggregate([
        {"$facet": {
            "facet_group": stages
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

def getAsignacion(request):
    item = request.POST.get('item') if request.POST.get('item') != None else 'asign'
    print('Itemisky: ' + item)
    mongo = Mongo("audit_facturas_0")
    if item == 'asign':
        datos = mongo.aggregate([
            # {"$match": {"fecha_radicado": {"$in": dates}} },
            # {"$project": {"fecha_radicado": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1, "estado_tecnica": 1, "estado_medica": 1, "estado_factura_conciliacion": 1}},
            {"$group": {"_id": "$usuario_auditoria_tecnica", "total": {"$sum": 1}} }
        ])
        return HttpResponse(datos, content_type="application/json")
    elif item == 'estados':
        tecnico = request.POST.get('tecnico')
        datos = mongo.aggregate([
            {"$match": {"usuario_auditoria_tecnica": tecnico} },
            # {"$project": {"fecha_radicado": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1, "estado_tecnica": 1, "estado_medica": 1, "estado_factura_conciliacion": 1}},
            {"$group": {"_id": "$estado_tecnica", "total": {"$sum": 1}} }
        ])
        return HttpResponse(datos, content_type="application/json")
    elif item == 'fechas':
        tecnico = request.POST.get('tecnico')
        criterio = {"$ne": ""} if tecnico == '-alltec-' else tecnico
        datos = mongo.aggregate([
            {"$facet": {"puntos": [
                {"$match": {"usuario_auditoria_tecnica": criterio} },
                {"$group": {"_id": "$fecha_radicado", "total": {"$sum": 1}} },
                {"$sort": {"_id": 1}}
            ]}}
        ])
        return HttpResponse(datos, content_type="application/json")
    elif item == 'facturas':
        tecnico = request.POST.get('tecnico')
        criterio = {"$ne": ""} if tecnico == '-alltec-' else tecnico
        fecha = request.POST.get('fecha')
        dates = str(fecha).split('|')
        # datos = mongo.aggregate([
        #     {"$match": {"fecha_radicado": {"$in": dates}, "usuario_auditoria_tecnica": criterio} },
        #     {"$project": {"fecha_radicado": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1, "estado_tecnica": 1, "estado_medica": 1, "estado_factura_conciliacion": 1, "usuario_auditoria_tecnica": 1, "usuario_auditoria_medica": 1, "total_glosas": 1}},
        #     {"$sort": {"consecutivo_radica": 1}},
        #     # {"$limit": 100}
        # ])
        kfields = {"fecha_radicado": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1, "estado_tecnica": 1, "estado_medica": 1, "estado_factura_conciliacion": 1, "usuario_auditoria_tecnica": 1, "usuario_auditoria_medica": 1, "total_glosas": 1}
        korden = [("consecutivo_radica", 1)]
        datos = mongo.find(filtro={"fecha_radicado": {"$in": dates}, "usuario_auditoria_tecnica": criterio}, pro=kfields, orden=korden)
        return HttpResponse(datos, content_type="application/json")
    elif item == 'search':
        filtro = {}
        hdata = False
        if request.POST.get('contrato') != None:
            filtro['numero_contrato'] = str(request.POST.get('contrato'))
            hdata = True
        if request.POST.get('factura') != None:
            filtro['factura'] = str(request.POST.get('factura'))
            hdata = True
        if request.POST.get('rsocial') != None:
            filtro['razon_social'] = {"$regex": str(request.POST.get('rsocial')), "$options": "i"}
            hdata = True
        if hdata:
            mongo = Mongo("audit_facturas_0")
            datos = mongo.aggregate([
                {"$match": filtro },
                {"$project": {"fecha_radicado": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1, "estado_tecnica": 1, "estado_medica": 1, "estado_factura_conciliacion": 1, "usuario_auditoria_tecnica": 1, "usuario_auditoria_medica": 1}},
            ])
            return HttpResponse(datos, content_type="application/json")
        else:
            return HttpResponse([], content_type="application/json")

def addOneTecnico(request):
    oid = request.POST.get('oid')
    tecnico = request.POST.get('tecnico')
    mongo = Mongo("audit_facturas_0")
    rs = mongo.updateOne({"_id": ObjectId(oid)}, {"usuario_auditoria_tecnica": tecnico}, False)
    status = 'success' if rs else 'failed'
    return JsonResponse({'status': status, 'msn': 'Welcome to morfee!'})

def getFacturasPoint(request):
    frad = request.POST.get('fecha')
    nit = request.POST.get('nit')
    periodo = request.POST.get('periodo')
    user = request.POST.get('user')
    filtro = {}
    dates = str(frad).split('|')
    filtro['fecha_radicado'] = {"$in": dates}
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if user != "":
        kuser = "" if user == '(Vacio)' else user
        filtro['usuario_auditoria_tecnica'] = kuser
    stages = []
    stages.append({"$match": filtro })
    stages.append({"$project": {"fecha_radicado": 1, "usuario_auditoria_tecnica": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1, "estado_tecnica": 1, "estado_medica": 1, "estado_factura_conciliacion": 1}})
    mongo = Mongo("audit_facturas_0")
    datos = mongo.aggregate([
        {"$facet": {
            "repu": stages
        }}]
    )
    return HttpResponse(datos, content_type="application/json")

def getFacturacionVue(request):
    mongo = Mongo("audit_facturas_0")
    datos = mongo.aggregate([
        {"$project": {"fecha_radicado": 1, "numero_recepcion": 1, "numero_contrato": 1, "fecha_expedicion": 1, "tipo_contrato": 1, "modalidad_contrato": 1, "valor_contrato": 1, "nit": 1, "digito_verificacion": 1, "codigo_prestador": 1, "razon_social": 1, "consecutivo_radica": 1, "factura": 1, "fecha_radicado": 1, "usuario_radica": 1, "valor_neto": 1}},


    ])
    return HttpResponse(datos, content_type="application/json")

def getFacturaRef(request):
    factura = request.POST.get('factura')
    mongo = Mongo("audit_facturas_0")
    dato = mongo.findOne({'factura': factura})
    return HttpResponse(dato, content_type="application/json")

def getDataPrestador(request):
    pass
    # coleccion = "audit_facturas_0"
    # mongo = Mongo(coleccion)
    # datos = mongo.aggregate([
    #     {"$project": {"created": {"$dateToString": {"format": "%Y-%m-%d", "date": "$_id"}}}},
    #     {"$match": {"crx": {"$exists": False}}},
    #     # {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "_id"}}, "total": {"$sum": 1}}},
    #     {"$group": {"_id": "$created", "total": {"$sum": 1}}}
    # ])
    # return HttpResponse(datos, content_type="application/json")

@login_required(login_url='/login/')
def pooja(request):
    print('Path media root ▼')
    # print(settings.MEDIA_ROOT)
    # for i in os.listdir(str(settings.MEDIA_ROOT)):
    #     os.remove(str(settings.MEDIA_ROOT)+'/'+i)
        
    # if request.method == 'POST' and request.FILES['file']:
    #     period=request.POST.get('period')
    #     delimeter=request.POST.get('delimeter')

    #     myfile = request.FILES['file']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
        
    #     print(filename)
    #     try:
    #         if delimeter=="Default":
    #             if str(filename).split('.')[1]=='csv' or str(filename).split('.')[1]=='txt':
    #                 df = pd.read_csv(fs.open(filename))
    #             elif str(filename).split('.')[1]=='xlsx' or str(filename).split('.')[1]=='xls':
    #                 df = pd.read_excel(fs.open(filename))
    #             elif str(filename).split('.')[1]=='json':
    #                 df=json.load(fs.open(filename))
    #             else:
    #                 return render(request, 'error.html')
    #         elif str(filename).split('.')[1]=='csv' or str(filename).split('.')[1]=='txt':
    #             df = pd.read_csv(fs.open(filename),sep=delimeter)
    #         elif str(filename).split('.')[1]=='xlsx' or str(filename).split('.')[1]=='xls':
    #             df = pd.read_excel(fs.open(filename),sep=delimeter)
    #         elif str(filename).split('.')[1]=='json':
    #             df=json.load(fs.open(filename))
    #         else:
    #             return render(request, 'auditorias/pooja/error.html')
    #     except:
    #         return render(request, 'auditorias/pooja/error.html')
            
    #     print(df)
    #     try:
    #         os.remove(str(fs.open(filename)))
    #     except:
    #         pass

    #     # conn = MongoClient('mongodb://localhost:27017')
    #     conn = MongoClient("mongodb+srv://carvi:ac2502412@sgsss.yv4ar.gcp.mongodb.net/import?authSource=admin") # /?retryWrites=true&w=majority")
    #     print("Connected successfully!!!")

    #     db = conn['testdb']
    #     print(str(filename))
    #     collection = db[str(filename).split('.')[0]]
        
    #     if str(filename).split('.')[1]=='csv' or str(filename).split('.')[1]=='txt' or  str(filename).split('.')[1]=='xlsx' or str(filename).split('.')[1]=='xls':
    #         collection.insert_many(df.to_dict(orient='records'))
    #     elif str(filename).split('.')[1]=='json':
    #         collection.insert_many(df)
        
    #     collection.update_many({},{"$set": {"period":period}})

    #     return render(request, 'auditorias/pooja/success.html')
    return render(request, 'auditorias/pooja/index.html')

@login_required(login_url='/login/')
def sispro(request):
    driver = '{MSOLAP}'
    server = 'cubos.sispro.gov.co'
    database = 'CU_Estadisticas Afiliados a Salud'
    cube = 'CU_Estadisticas Afiliados a Salud General'
    user = "sispro.local\\usr_bdua"
    passw = 'usr_bdua'
    # connStr = server + ' ' + database + ' ' + cube
    rs = 'before'
    # try:
    #     # conexion = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE'+database+';CUBE='+cube+';UID='+user+';PWD='+passw)
    #     # conexion = pyodbc.connect('DRIVER={MSOLAP};User=myuseraccount;Password=mypassword;URL=http://localhost/OLAP/msmdpump.dll;')
    #     conexion = pyodbc.connect('DRIVER={MSOLAP};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+passw)
    #     rs = 'conexion exitosa'

    # except:
    #     rs = 'error al conectar'
    return render(request, 'auditorias/sispro.html', {'mensaje': rs})

@login_required(login_url='/login/')
def qr_example(request):
    response = HttpResponse(content_type="image/png")
    content = "A two-dimensional bar code used for its fast readability and comparatively large storage capacity. It consists of black squares arranged in a square."
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(content)
    qr.make(fit=True)
    qr.make_image().save(response, 'PNG')
    return response

@login_required(login_url='/login/')
def qrList(request):
    return render(request, 'auditorias/qr_example.html')

@login_required(login_url='/login/')
def actas(request):
    return render(request, 'auditorias/qr_actas.html')

def vueListQR(request):
    mongo = Mongo("audit_qrlist_0")
    datos = mongo.find({}, pro={'factura': 1, 'auditor': 1, 'fecha': 1, 'estado': 1, 'valor': 1})
    return HttpResponse(datos, content_type="application/json")

def vueFacturaQR(request, code):
    mongo = Mongo('audit_qrlist_0')
    rl = mongo.findOne({'_id': ObjectId(code)})
    dato = json.loads(rl)
    # print(dato)
    # content = f"Código: {code}\n Factura: {dato.factura}\n Auditor: {dato.auditor}\n Fecha: {dato.fecha}\n Estado: {dato.estado}\n Valor: {dato.valor}"
    content = f"Código: {code}\nFactura: {dato['factura']}\nAuditor: {dato['auditor']}\nFecha: {dato['fecha']}\nEstado: {dato['estado']}\nValor: {dato['valor']}"
    response = HttpResponse(content_type="image/png")
    # content = "A two-dimensional bar code used for its fast readability and comparatively large storage capacity. It consists of black squares arranged in a square."
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(content)
    qr.make(fit=True)
    qr.make_image().save(response, 'PNG')
    return response

def vueSaveQR(request):
    data = {'factura': request.POST.get('factura'), 'auditor': request.POST.get('auditor'), 'fecha': request.POST.get('fecha'), 'estado': request.POST.get('estado'), 'valor': request.POST.get('valor')}
    mongo = Mongo('audit_qrlist_0')
    rs = mongo.insertOne(data)
    return HttpResponse(rs, content_type="application/json")

def vueListActasQR(request):
    mongo = Mongo("audit_qractas_0")
    datos = mongo.find({'tipo': 'qr'}, pro={'tipo': 1, 'hash': 1, 'cod': 1, 'dep': 1, 'mun': 1, 'pre': 1, 'nit': 1, 'aud': 1, 'total': 1, 'facs': 1, 'rads': 1, 'history': 1, 'create': 1, 'update': 1})
    return HttpResponse(datos, content_type="application/json")

def vueActaRef(request):
    code = request.POST.get('codigo')
    mongo = Mongo("audit_qractas_0")
    datos = mongo.find({'hash': code}, pro={'tipo': 1, 'hash': 1, 'cod': 1, 'dep': 1, 'mun': 1, 'pre': 1, 'nit': 1, 'aud': 1, 'total': 1, 'facs': 1, 'rads': 1, 'fir': 1, 'car': 1, 'obs': 1, 'history': 1, 'create': 1, 'update': 1, 'k_rad': 1, 'f_rad': 1, 'f_ate': 1, 'num_pac': 1, 'nom_pac': 1, 'k_fac': 1, 'k_val': 1, 'g_val': 1, 'g_cod': 1, 'g_mot': 1, 'g_eps': 1, 'g_ips': 1, 'g_pen': 1, 'k_pay': 1})
    return HttpResponse(datos, content_type="application/json")

def vueActaCross(request):
    fts = request.POST.get('facturas')
    facturas = str(fts).split('|')
    mongo = Mongo("audit_glosas_0")
    datos = mongo.aggregate([
        {"$project": {"_id": 0, "numero_factura": 1, "glosa": 1, "concepto": 1} },
        {"$match": {"numero_factura": {"$in": facturas}} },
        {"$group": {"_id": "$numero_factura", "glosa": {"$first": "$glosa"}, "concepto": {"$first": "$concepto"} }},
    ])
    return HttpResponse(datos, content_type="application/json")

def vueImageQR(request, code):
    mongo = Mongo('audit_qractas_0')
    rl = mongo.findOne({'_id': ObjectId(code), 'tipo': 'qr'})
    dato = json.loads(rl)
    content = f"Código de seguridad: <{dato['hash']}>\nCódigo del acta: <{dato['cod']}>\nNIT: <{dato['nit']}>\nPrestador: <{dato['pre']}>\nAuditor: <{dato['aud']}>\nRegistro: <{dato['create']}>\nValor: <{dato['total']}>"
    response = HttpResponse(content_type="image/png")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(content)
    qr.make(fit=True)
    qr.make_image().save(response, 'PNG')
    return response

def vueSaveActa(request):
    raw = request.POST.get('datosqr')
    docs = json.loads(raw)
    ref = docs[0]['_id']
    docs[0]['_id'] = ObjectId(ref)
    print(docs)
    mongo = Mongo('audit_qractas_0')
    rs = mongo.insertMany(docs)
    rs = {'status': 'success'}
    return JsonResponse(rs)
    return HttpResponse(rs, content_type="application/json")

def vueSaveEditActa(request):
    kii = request.POST.get('hash')
    mongo = Mongo('audit_qractas_0')
    for key in request.POST:
        raw = request.POST.get(key)
        if key == 'mainqr':
            mqr = json.loads(raw)
            mongo.updateOne({'_id': ObjectId(kii), 'tipo': 'qr'}, mqr)
        if key == 'datosqr':
            docs = json.loads(raw)
            mongo.insertMany(docs)
        if key[0:5] == 'edit_':
            doc = json.loads(raw)
            fac = key[5:]
            mongo.updateOne({'hash': kii, 'k_fac': fac, 'tipo': 'data'}, doc)
        if key[0:5] == 'elim_':
           mongo.deleteOne({'hash': kii, 'k_fac': raw, 'tipo': 'data'}) 
        print(request.POST[key])
    return JsonResponse({'status': 'success'})

def vueCodex(request):
    codex = str(ObjectId())
    return HttpResponse(codex, content_type="application/json")

def vueSearchFac(request):
    cofac = request.POST.get('factura')
    radicado = request.POST.get('radicado')
    cash = request.POST.get('cash')
    rad_num = int(radicado)
    rad_str = str(radicado)
    mongo = Mongo('audit_facturas_0')
    # 'factura': cofac
    filtro = {'numero_radicacion': {"$in": [rad_num, rad_str]}}
    if cash == 'has-value':
        filtro['total_glosas'] = {"$gt": 0}
    # rs = mongo.find(filtro, pro={'factura': 1, 'consecutivo_radica': 1, 'numero_radicacion': 1, 'valor_factura': 1, 'nit': 1, 'razon_social': 1, 'numero_contrato': 1, 'total_glosas': 1})
    rs = mongo.aggregate([
        {"$facet": {"facturas": [
            {"$match": filtro},
            {"$project": {'factura': 1, 'fecha_radicado': 1, 'consecutivo_radica': 1, 'numero_radicacion': 1, 'valor_factura': 1, 'valor_neto': 1, 'nit': 1, 'razon_social': 1, 'numero_contrato': 1, 'total_glosas': 1} },
            {"$lookup": {"from": "audit_qractas_0", "localField": "factura", "foreignField": "k_fac", "as": "itachi"} },
        ]}}
    ])
    return HttpResponse(rs, content_type="application/json")

def vueCifras(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    filtro = {}
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    mongo = Mongo('audit_facturas_0')
    core = []
    concilia = []
    if bool(filtro):
        core.append({"$match": filtro})
        concilia.append({"$match": filtro})
    core.append({"$group": {"_id": "$nit", "prestador": {"$first": "$razon_social"}, "total": {"$sum": "$valor_factura"}, "sum_glosas": {"$sum": "$total_glosas"}, "sum_pagar": {"$sum": "$total_pagar"} }})
    core.append({"$sort": {'total': -1} })
    concilia.append({"$group": {"_id": None, "eps": {"$sum": "$valor_total_acepta_eps"}, "ips": {"$sum": "$valor_total_acepta_ips"} } })
    datos = mongo.aggregate([
        {"$facet": {
            "repu": core, 
            "concilia": concilia,
            "general": [
                {"$match": filtro },
                {"$project": {'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, 'valor_factura': 1, 'total_glosas': 1, 'total_pagar': 1 } },
                {"$group": {"_id": "$periodo", "total": {"$sum": "$valor_factura"}, "sum_glosas": {"$sum": "$total_glosas"}, "sum_pagar": {"$sum": "$total_pagar"}, "sum_fac": {"$sum": 1} }},
                {"$sort": {"_id": 1} }
            ]
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

def vuePeriodos(request):
    anio = request.POST.get('anio')
    nit = request.POST.get('nit')
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$project": {'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, 'valor_factura': 1, 'total_glosas': 1, 'total_pagar': 1 } },
        {"$group": {"_id": "$periodo", "total": {"$sum": "$valor_factura"}, "sum_glosas": {"$sum": "$total_glosas"}, "sum_pagar": {"$sum": "$total_pagar"}, "sum_fac": {"$sum": 1} }},
        {"$sort": {"_id": 1} }
    ])
    return HttpResponse(datos, content_type="application/json")

def vueSocial(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    auditor = request.POST.get('auditor')
    nit = request.POST.get('nit')
    periodo = request.POST.get('periodo')
    filtro = {}
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    stages = []
    if bool(filtro):
        stages.append({"$match": filtro})
    stages.append({"$group": {"_id": "$nit", "prestador": {"$first": "$razon_social"}, "count": {"$sum": 1} }})
    stages.append({"$sort": {"count": -1} })
    stages.append({"$limit": 100})
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate(stages)
    return HttpResponse(datos, content_type="application/json")

def vueRegimen(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    filtro = {}
    stages = []
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    if bool(filtro):
        stages.append({"$match": filtro})
    stages.append({"$group": {"_id": "$tipo_contrato", "total": {"$sum": 1}, "factura": {"$sum": "$valor_factura"} }})
    stages.append({"$sort": {'total': 1} })
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$facet": {"repu": stages}}
    ])
    return HttpResponse(datos, content_type="application/json")

def vueCase(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    filtro = {}
    stages = []
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    if bool(filtro):
        stages.append({"$match": filtro})
    stages.append({"$group": {"_id": "$estado_tecnica", "total": {"$sum": 1} }})
    stages.append({"$sort": {'total': 1} })
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$facet": {"repu": stages}}
    ])
    return HttpResponse(datos, content_type="application/json")

def vueCaseSelectBar(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    pagina = int(request.POST.get('pagina'))
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    estado = request.POST.get('estado')
    cantidad = 50
    salto = cantidad * (pagina - 1)
    filtro = {}
    filtro['estado_tecnica'] = estado
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    stages = []
    stages.append({"$match": filtro })
    stages.append({"$project": {"numero_radicacion":1, "razon_social":1, "factura":1, "fecha_radicado":1, "usuario_auditoria_tecnica":1, "estado_tecnica":1, "tipo_contrato":1, "departamento":1, "municipio":1}})
    stages.append({'$skip': salto})
    stages.append({'$limit': cantidad + 1})
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'slice': stages,
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def vueConciliacion(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    filtro = {}
    grupo = {}
    stages = []
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    grupo = {"_id": {"per": "$periodo", "stt": "$formi"}, "total": {"$sum": 1}, "suma": {"$sum": "$total_glosas"}, "prd": {"$first": "$periodo"} }
    if nit != "":
        filtro['doc'] = str(nit)
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor

    stages.append({"$project": {'fecha_radicado': 1, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, 'doc': {"$toString": "$nit"}, 'formi': {'$cond': [{'$eq': [{'$add': ['$valor_total_acepta_eps', '$valor_total_acepta_ips']}, '$total_glosas'] }, 'Conciliado', 'Pendiente por conciliar']}, 'total_glosa': 1, 'razon_social': 1, 'departamento': 1, 'municipio': 1 } })
    if bool(filtro):
        stages.append({"$match": filtro})
    stages.append({"$group": grupo })
    stages.append({"$sort": {'prd': 1} })
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$facet": {"repu": stages}}
    ])
    return HttpResponse(datos, content_type="application/json")

def vueConciliacionBar(request):
    depto = request.POST.get('depto')
    tcc = request.POST.get('tcc')
    pagina = int(request.POST.get('pagina'))
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    barra = request.POST.get('barra')
    cantidad = 50
    salto = cantidad * (pagina - 1)
    filtro = {}
    if depto != "":
        filtro['departamento'] = depto
    if tcc != "":
        filtro['tipo_contrato'] = tcc
    if barra != 'glosado':
        filtro['formi'] = barra
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['doc'] = str(nit)
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    stages = []
    stages.append({"$project": {'fecha_radicado': 1, 'razon_social': 1, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, 'doc': {"$toString": "$nit"}, 'formi': {'$cond': [{'$eq': [{'$add': ['$valor_total_acepta_eps', '$valor_total_acepta_ips']}, '$total_glosas'] }, 'ready', 'pending']}, 'total_glosa': 1, 'usuario_auditoria_tecnica': 1, 'valor_total_acepta_eps': 1, 'valor_total_acepta_ips': 1, "numero_radicacion": 1, "factura": 1, "estado_tecnica": 1, "tipo_contrato": 1, "departamento": 1, "municipio": 1 } });
    stages.append({"$match": filtro })
    stages.append({'$skip': salto})
    stages.append({'$limit': cantidad + 1})
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'slice': stages,
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def vueConciliaSlice(request):
    auditor = request.POST.get('auditor')
    periodo = request.POST.get('periodo')
    nit = request.POST.get('nit')
    stt_fac = request.POST.get('stt_fac')
    pagina = int(request.POST.get('pagina'))
    cantidad = int(request.POST.get('cantidad'))
    salto = cantidad * (pagina - 1)
    filtro = {'estado_factura_conciliacion': stt_fac}
    stages = []
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if auditor != "":
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-void-' else auditor
    stages.append({"$match": filtro})
    stages.append({'$project': {'_id':0, 'numero_recepcion':1, 'estado_factura_conciliacion': 1, 'numero_radicacion':1, 'valor_factura':1, 'numero_contrato':1, 'tipo_contrato':1, 'modalidad_contrato':1, 'nit':1, 'razon_social':1, 'factura':1, 'fecha_radicado':1, 'usuario_radica':1, 'usuario_auditoria_tecnica':1, 'pos':1, 'estado_tecnica':1, 'case':1, 'valor_total_acepta_eps':1, 'valor_total_acepta_ips':1} })
    stages.append({'$skip': salto})
    stages.append({'$limit': cantidad + 1})
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate(stages)
    return HttpResponse(datos, content_type="application/json")

def allEntities(request):
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'tcc': [
                {"$group": {"_id": "$tipo_contrato"} },
                {"$sort": {"_id": 1}}
            ],
            'ipss': [
                {"$group": {"_id": "$nit", "prestador": {"$first": "$razon_social"}} },
                {"$sort": {"prestador": 1} },
            ],
            'times': [
                {"$project": {'periodo': {"$substr": ["$fecha_radicado", 0, 7]} } },
                {"$group": {"_id": '$periodo', 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ],
            'auditores': [
                {"$group": {"_id": '$usuario_auditoria_tecnica', 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ],
            'deptos': [
                {"$group": {"_id": "$departamento", 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ]
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def codeglosa(request):
    build = request.POST.get('build')
    nit = request.POST.get('nit')
    filtro = {}
    if nit:
        filtro['doc'] = str(nit)
    
    stages = [];
    stages.append({"$project": {'doc': {"$toString": "$numero_identificacion"}, 'vcode': {"$substr": ["$glosa", 0, 3]}, 'vbase': {"$substr": ["$glosa", 0, 1]}, 'vnum': {"$convert": {"input": "$valor_glosa", "to": "double", "onError": 0, "onNull": 0}} } })
    if filtro:
        stages.append({"$match": filtro})
    stages.append({"$group": {"_id": "$vbase", "total": {"$sum": 1}, "suma": {"$sum": "$vnum"}} })
    stages.append({"$sort": {"_id": 1} })
    mongo = Mongo('audit_glosas_0')
    if build == 'yes':
        datos = mongo.aggregate([
            {'$facet': {
                'general': stages,
                'ipss': [
                    {"$project": {'doc': {"$toString": "$numero_identificacion"}, 'razon_social': 1} },
                    {"$group": {"_id": "$doc", "pre": {"$first": "$razon_social"}, "total": {"$sum": 1}} },
                    {"$sort": {"pre": 1} }
                ]
            }},
        ])
        return HttpResponse(datos, content_type="application/json")
    else:
        datos = mongo.aggregate([ {'$facet': {'general': stages} } ])
        return HttpResponse(datos, content_type="application/json")

def detalleglosa(request):
    grupo = request.POST.get('grupo')
    nit = request.POST.get('nit')
    filtro = {}
    filtro['vbase'] = {'$regex': '^[^0-9]'} if grupo == '0' else str(grupo)
    if nit:
        filtro['doc'] = str(nit)
    mongo = Mongo('audit_glosas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'general': [
                {"$project": {'glosa': 1, 'doc': {"$toString": "$numero_identificacion"}, 'vcode': {"$substr": ["$glosa", 0, 3]}, 'vbase': {"$substr": ["$glosa", 0, 1]}, 'vnum': {"$convert": {"input": "$valor_glosa", "to": "double", "onError": 0, "onNull": 0}} } },
                {"$match": filtro}, 
                {"$group": {"_id": "$vcode", "texto": {"$first": "$glosa"}, "total": {"$sum": 1}, "suma": {"$sum": "$vnum"}} },
                {"$sort": {"_id": 1} },
            ],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def getFiltros(request):
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'ipss': [
                {"$group": {"_id": "$nit", "prestador": {"$first": "$razon_social"}} },
                {"$sort": {"prestador": 1} },
            ],
            'times': [
                {"$project": {'periodo': {"$substr": ["$fecha_radicado", 0, 7]} } },
                {"$group": {"_id": '$periodo', 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ],
            'users': [
                {"$group": {"_id": "$usuario_auditoria_tecnica", 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ]
        }},
    ])
    return HttpResponse(datos, content_type="application/json")


def estadoTecnicaInit(request):
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'estado': [
                {"$group": {"_id": "$estado_tecnica", "total": {"$sum": 1} } }
            ],
            'pos': [
                {"$group": {"_id": "$pos", "total": {"$sum": 1} } }
            ],
            'ipss': [
                {"$group": {"_id": "$nit", "prestador": {"$first": "$razon_social"}} },
                {"$sort": {"prestador": 1} },
            ],
            'times': [
                {"$project": {'periodo': {"$substr": ["$fecha_radicado", 0, 7]} } },
                {"$group": {"_id": '$periodo', 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ],
            'users': [
                {"$group": {"_id": "$usuario_auditoria_tecnica", 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ],
            'deptos': [
                {"$group": {"_id": "$departamento", 'total': {"$sum": 1} } },
                {"$sort": {"_id": 1} }
            ]
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def estadoTecnica(request):
    depto = request.POST.get('depto')
    nit = request.POST.get('nit')
    periodo = request.POST.get('periodo')
    user = request.POST.get('user')
    pos = request.POST.get('pos')
    filtro = {}
    aux = False
    if depto != "":
        filtro['departamento'] = depto
        aux = True
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
        aux = True
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
        aux = True
    if user != "":
        kuser = "" if user == '(Vacio)' else user
        filtro['usuario_auditoria_tecnica'] = kuser
        aux = True
    if len(pos) > 0:
        filtro['pos'] = pos
        aux = True
    mongo = Mongo('audit_facturas_0')
    if aux:
        datos = mongo.aggregate([
            {"$match": filtro },
            {'$facet': {
                'estado': [{"$group": {"_id": "$estado_tecnica", "total": {"$sum": 1} } }],
                'pos': [{"$group": {"_id": "$pos", "total": {"$sum": 1} } }],
            }},
        ])
        return HttpResponse(datos, content_type="application/json")
    else:
        datos = mongo.aggregate([
            {'$facet': {
                'estado': [{"$group": {"_id": "$estado_tecnica", "total": {"$sum": 1} } }],
                'pos': [{"$group": {"_id": "$pos", "total": {"$sum": 1} } }],
            }},
        ])
        return HttpResponse(datos, content_type="application/json")

def estadoTecnicaSlice(request):
    pagina = int(request.POST.get('pagina'))
    depto = request.POST.get('depto')
    nit = request.POST.get('nit')
    periodo = request.POST.get('periodo')
    user = request.POST.get('user')
    pos = request.POST.get('pos')
    estado = request.POST.get('estado')
    cantidad = 50
    salto = cantidad * (pagina - 1)
    filtro = {}
    filtro['estado_tecnica'] = estado
    if depto != "":
        filtro['departamento'] = depto
    if len(periodo) > 0:
        filtro['fecha_radicado'] = {"$regex": periodo, "$options": "i"}
    if nit != "":
        filtro['nit'] = {"$in": [str(nit), int(nit)]}
    if user != "":
        kuser = "" if user == '(Vacio)' else user
        filtro['usuario_auditoria_tecnica'] = kuser
    if len(pos) > 0:
        filtro['pos'] = pos
    stages = []
    stages.append({"$match": filtro })
    stages.append({"$project": {"numero_radicacion":1, "razon_social":1, "factura":1, "fecha_radicado":1, "usuario_auditoria_tecnica":1, "estado_tecnica":1, "departamento":1, "municipio":1}})
    stages.append({'$skip': salto})
    stages.append({'$limit': cantidad + 1})
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {'$facet': {
            'slice': stages,
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def kpi_periodos(request):
    vigencia = request.POST.get('vigencia')
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$addFields": {"derr": {"$toDate": "1900-01-01"}, 'tsum': {"$sum":['$valor_total_acepta_eps', '$valor_total_acepta_ips']} }},
        {"$addFields": {"raw": {"$convert": {"input": "$fecha_radicado", "to": "date", "onError": "$derr", "onNull": "$derr"}} }},
        {"$project": {'anio': {"$year": "$raw"}, 'mes': {"$month": "$raw"}, 'dia': {"$dayOfMonth": "$raw"}, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, "fecha_radicado": 1, 'valor_factura': 1, 'total_glosas': 1, 'total_glosa': 1, 'total_pagar': 1, 'razon_social': 1, 'tsum': 1, "formi":{'$cond': [{'$eq': ['$tsum', '$total_glosas'] }, 'equal', 'diff']} }},
        {'$facet': {
            'monthead': [
                {"$match": {'anio': int(vigencia)}},
                {"$group": {"_id": {"per": "$periodo", "formi": "$formi"}, "total": {"$sum": 1}, "sglo": {"$sum": "$total_glosas"}, "seip": {"$sum": "$tsum"} }},
                {"$sort": {"_id": 1}}
                # {"$group": {"_id": "$periodo", "total": {"$sum": 1} }},
                # {"$limit": 10},
            ],
            'anios': [
                {"$group": {"_id": "$anio", "total": {"$sum": 1}} }
            ]
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

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
        {"$addFields": {'anio': {"$year": "$raw"}, 'mes': {"$month": "$raw"}, 'dia': {"$dayOfMonth": "$raw"}, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, "formi":{'$cond': [{'$eq': ['$tsum', '$total_glosas'] }, 'Conciliado', 'Sin conciliar']} }},
        {"$match": filtro },
        {'$facet': {
            'periodo': [
                {"$group": {"_id": "$formi", "total": {"$sum": 1}, "sglo": {"$sum": "$total_glosas"}, "seip": {"$sum": "$tsum"} }},
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

def kpi_control_fechas(request):
    pagina = int(request.POST.get('pagina')) if request.POST.get('pagina') else 1
    cantidad = 50
    salto = cantidad * (pagina - 1)
    vigencia = request.POST.get('vigencia')
    mes = request.POST.get('mes')
    dia = int(request.POST.get('dia')) if request.POST.get('dia') else 0
    filtro = {'anio': int(vigencia), 'mes': int(mes)}
    auditor = request.POST.get('f_auditor')
    estado = request.POST.get('f_estado')
    conci = request.POST.get('f_conci')
    fechas = request.POST.get('fechas')
    if dia > 0:
        filtro['dia'] = {'$lte': dia}
    if auditor:
        filtro['usuario_auditoria_tecnica'] = "" if auditor == '-empty-' else auditor
    if estado:
        filtro['estado_tecnica'] = "" if estado == '-empty-' else estado
    if conci:
        filtro['formi'] = conci
    if fechas:
        if fechas.find('|') >= 0:
            filtro['fecha_radicado'] = {"$in": fechas.split('|')}
        else:
            filtro['fecha_radicado'] = fechas
    mongo = Mongo('audit_facturas_0')
    datos = mongo.aggregate([
        {"$addFields": {"derr": {"$toDate": "1900-01-01"}, 'tsum': {"$sum":['$valor_total_acepta_eps', '$valor_total_acepta_ips']} }},
        {"$addFields": {"raw": {"$convert": {"input": "$fecha_radicado", "to": "date", "onError": "$derr", "onNull": "$derr"}} }},
        {"$addFields": {'anio': {"$year": "$raw"}, 'mes': {"$month": "$raw"}, 'dia': {"$dayOfMonth": "$raw"}, 'periodo': {"$substr": ["$fecha_radicado", 0, 7]}, "formi":{'$cond': [{'$eq': ['$tsum', '$total_glosas'] }, 'Conciliado', 'Sin conciliar']} }},
        {"$match": filtro },
        {"$project": {'razon_social':1, 'factura':1, 'consecutivo_radica':1, 'fecha_radicado':1, 'usuario_auditoria_tecnica':1, 'estado_tecnica':1, 'valor_neto':1, 'valor_total_acepta_eps':1, 'valor_total_acepta_ips':1, 'total_glosa':1, 'total_glosas':1, 'formi': 1} },
        {'$facet': {
            'facturas': [
                {"$sort": {"fecha_radicado": 1} },
                {'$skip': salto},
                {'$limit': cantidad + 1}
            ],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

# Nuevo comentario...