from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_frontier.mongo import Mongo
import pandas as pd
import json, datetime
from . import forms, models
from django.db import connection

# SECTION USERS
@login_required(login_url='/login/')
def user_list(request):
    datos = models.UserMorfee.objects.all()
    return render(request, 'users/user_list.html', {'datos': datos})

@login_required(login_url='/login/')
def user_preselect(request):
    return render(request, 'users/user_preselect.html')

@login_required(login_url='/login/')
def user_add(request):
    if request.method == "POST":
        form = forms.UserMorfeeForm(request.POST)
        if form.is_valid():
            user = models.UserMorfee()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.cliente = models.AuthCliente.objects.get(pk=request.POST.get('cliente'))
            user.rol = models.AuthRol.objects.get(pk=request.POST.get('rol'))
            user.save()
            return redirect('ad_user_list')
        else:
            return render(request, 'users/user_add.html', {'form': form})
    else:
        return render(request, 'users/user_add.html', {'form': forms.UserMorfeeForm()})

@login_required(login_url='/login/')
def user_add_staff(request):
    if request.method == "POST":
        form = forms.UserStaffForm(request.POST)
        if form.is_valid():
            user = models.UserMorfee()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.is_staff = True
            user.save()
            return redirect('ad_user_list')
        else:
            return render(request, 'users/user_add_staff.html', {'form': form})
    else:
        return render(request, 'users/user_add_staff.html', {'form': forms.UserStaffForm()})

@login_required(login_url='/login/')
def user_edit(request, id):
    try:
        user = models.UserMorfee.objects.get(pk=id)
        plantilla = 'users/user_edit_staff.html' if user.is_superuser or user.is_staff else 'users/user_edit.html'
        if request.method == "POST":
            form = forms.UserEditStaffForm(request.POST, instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('ad_user_list')
            else:
                return render(request, plantilla, {'form': form, 'usuario': user})
        else:
            form = forms.UserEditStaffForm(instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(instance=user)
            return render(request, plantilla, {'form': form, 'usuario': user})
    except models.UserMorfee.DoesNotExist:
        return render(request, 'users/not_found.html', {'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})

@login_required(login_url='/login/')
def user_remove(request, id):
    try:
        user = models.UserMorfee.objects.get(pk=id)
        if not user.is_superuser:
            try:
                user.delete()
                return redirect('ad_user_list')
            except models.UserMorfee.DoesNotExist:
                return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi titulo', 'mensaje': 'No se pudo encontrar el registro solicitado, por lo tanto, no se puede eliminar, por favor consulte con el administrador del sitio.'})
        else:
            return redirect('ad_user_list')
    except models.UserMorfee.DoesNotExist:
        return render(request, 'users/not_found.html', {'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})


# SECTION CLIENTES
@login_required(login_url='/login/')
def cli_user_list(request):
    uid = request.user.cliente_id
    datos = models.UserMorfee.objects.filter(cliente_id=uid)
    return render(request, 'users/cli_user_list.html', {'datos': datos})

@login_required(login_url='/login/')
def cli_user_add(request):
    if request.method == "POST":
        form = forms.UserMorfeeForm(request.POST)
        if form.is_valid():
            user = models.UserMorfee()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.cliente = models.AuthCliente.objects.get(pk=request.POST.get('cliente'))
            user.rol = models.AuthRol.objects.get(pk=request.POST.get('rol'))
            user.save()
            return redirect('ad_ucli_list')
        else:
            return render(request, 'users/cli_user_add.html', {'form': form})
    else:
        return render(request, 'users/cli_user_add.html', {'form': forms.UserClientForm(request.user.cliente_id)})

@login_required(login_url='/login/')
def cli_user_edit(request, id):
    try:
        user = models.UserMorfee.objects.get(pk=id)
        if request.method == "POST":
            form = forms.UserEditStaffForm(request.POST, instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('ad_ucli_list')
            else:
                return render(request, 'users/cli_user_edit.html', {'form': form, 'usuario': user})
        else:
            # form = forms.UserClientEditForm(instance=user)
            form = forms.UserClientEditForm(instance=user, daky=request.user.cliente_id)
            return render(request, 'users/cli_user_edit.html', {'form': form, 'usuario': user})
    except models.UserMorfee.DoesNotExist:
        return render(request, 'users/not_found.html', {'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})

@login_required(login_url='/login/')
def cli_user_store(request):
    if request.method == "POST":
        form = forms.UserMorfeeForm(request.POST)
        if form.is_valid():
            user = models.UserMorfee()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.cliente = models.AuthCliente.objects.get(pk=request.POST.get('cliente'))
            user.rol = models.AuthRol.objects.get(pk=request.POST.get('rol'))
            user.save()
            return redirect('ad_user_list')
        else:
            return render(request, 'users/user_add.html', {'form': form})
    else:
        return render(request, 'users/user_add.html', {'form': forms.UserMorfeeForm()})

@login_required(login_url='/login/')
def changeLock(request):
    return render(request, 'users/change_lock.html')

@login_required(login_url='/login/')
def cliente_list(request):
    datos = models.AuthCliente.objects.all()
    return render(request, 'users/cliente_list.html', {'datos': datos})

@login_required(login_url='/login/')
def cliente_add(request):
    if request.method == "POST":
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            cli = models.AuthCliente()
            cli.cliente = request.POST.get('cliente')
            cli.direccion = request.POST.get('direccion')
            cli.correo = request.POST.get('correo')
            cli.contacto = request.POST.get('contacto')
            cli.modulos = "|".join(request.POST.getlist('modulos'))
            cli.is_indigena = 1 if request.POST.get('is_indigena') else None
            cli.save()
            diccionarios = models.Diccionario.objects.filter(tipo='template')
            for dc in diccionarios:
                n_dic = models.Diccionario()
                n_dic.modulo = dc.modulo
                n_dic.coleccion = dc.coleccion + str(cli.id)
                n_dic.alias = dc.alias
                n_dic.campos = dc.campos
                n_dic.has_data = 0
                n_dic.type_head = dc.type_head
                n_dic.propietario = dc.propietario
                n_dic.cliente = cli
                n_dic.reglas = dc.reglas
                n_dic.tipo = 'final'
                n_dic.save()
            return redirect('ad_cliente_list')
        else:
            return render(request, 'users/cliente_add.html', {'form': form})
    else:
        return render(request, 'users/cliente_add.html', {'form': forms.ClienteForm()})

@login_required(login_url='/login/')
def cliente_edit(request, id):
    try:
        cli = models.AuthCliente.objects.get(pk=id)
        if request.method == "POST":
            form = forms.ClienteForm(request.POST)
            if form.is_valid():
                cli.cliente = request.POST.get('cliente')
                cli.direccion = request.POST.get('direccion')
                cli.correo = request.POST.get('correo')
                cli.contacto = request.POST.get('contacto')
                cli.modulos = "|".join(request.POST.getlist('modulos'))
                cli.is_indigena = 1 if request.POST.get('is_indigena') else None
                cli.save()
                return redirect('ad_cliente_list')
            else:
                inicio = {'cliente': request.POST.get('cliente'), 'direccion': request.POST.get('direccion'), 'correo': request.POST.get('correo'), 'contacto': request.POST.get('contacto'), 'modulos': "|".join(request.POST.getlist('modulos'))}
                return render(request, 'users/cliente_edit.html', {'form': forms.ClienteForm(initial=inicio), 'cliente': cli})
        else:
            inicio = {'cliente': cli.cliente, 'direccion': cli.direccion, 'correo': cli.correo, 'contacto': cli.contacto, 'modulos': cli.modulos.split("|"), 'is_indigena': cli.is_indigena}
            return render(request, 'users/cliente_edit.html', {'form': forms.ClienteForm(initial=inicio), 'cliente': cli})
    except models.AuthCliente.DoesNotExist:
        return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi título', 'mensaje': 'No se pudo encontrar el cliente solicitado, por favor consulte con el administrador del sitio.'})

# SECTION ROLES
@login_required(login_url='/login/')
def rol_list(request):
    datos = models.AuthRol.objects.all()
    return render(request, 'users/rol_list.html', {'datos': datos})

@login_required(login_url='/login/')
def rol_add(request):
    if request.method == "POST":
        form = forms.RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ad_rol_list')
        else:
            return render(request, 'users/rol_add.html', {'form': form})
    else:
        return render(request, 'users/rol_add.html', {'form': forms.RolForm()})

@login_required(login_url='/login/')
def rol_edit(request, id):
    try:
        role = models.AuthRol.objects.get(pk=id)
        if request.method == "POST":
            form = forms.RolForm(request.POST, instance=role)
            if form.is_valid():
                form.save()
                return redirect('ad_rol_list')
            else:
                return render(request, 'users/rol_edit.html', {'form': form, 'role': role})
        else:
            return render(request, 'users/rol_edit.html', {'form': forms.RolForm(instance=role), 'role': role})
    except models.AuthRol.DoesNotExist:
        return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi título', 'mensaje': 'No se pudo encontrar el rol solicitado, por favor consulte con el administrador del sitio.'})

@login_required(login_url='/login/')
def rol_remove(request, id):
    if request.user.is_staff:
        try:
            role = models.AuthRol.objects.get(pk=id)
            role.delete()
            return redirect('ad_rol_list')
        except models.AuthRol.DoesNotExist:
            return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi titulo', 'mensaje': 'No se pudo encontrar el registro solicitado, por lo tanto, no se puede eliminar, por favor consulte con el administrador del sitio.'})
    else:
        return redirect('inicio')

# SECTION MÓDULOS
@login_required(login_url='/login/')
def modulo_list(request):
    datos = models.AuthModulo.objects.all()
    return render(request, 'users/modulo_list.html', {'datos': datos})

@login_required(login_url='/login/')
def modulo_add(request):
    if request.method == "POST":
        form = forms.ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ad_modulo_list')
        else:
            return render(request, 'users/modulo_add.html', {'form': form})
    else:
        return render(request, 'users/modulo_add.html', {'form': forms.ModuloForm()})

@login_required(login_url='/login/')
def modulo_edit(request, id):
    try:
        modulo = models.AuthModulo.objects.get(pk=id)
        if request.method == "POST":
            form = forms.ModuloForm(request.POST, instance=modulo)
            if form.is_valid():
                form.save()
                return redirect('ad_modulo_list')
            else:
                return render(request, 'users/modulo_edit.html', {'form': form, 'modulo': modulo})
        else:
            return render(request, 'users/modulo_edit.html', {'form': forms.ModuloForm(instance=modulo), 'modulo': modulo})
    except models.AuthCliente.DoesNotExist:
        return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi título', 'mensaje': 'No se pudo encontrar el cliente solicitado, por favor consulte con el administrador del sitio.'})

@login_required(login_url='/login/')
def modulo_remove(request, id):
    if request.user.is_staff:
        try:
            modulo = models.AuthModulo.objects.get(pk=id)
            modulo.delete()
            return redirect('ad_modulo_list')
        except models.AuthModulo.DoesNotExist:
            return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi titulo', 'mensaje': 'No se pudo encontrar el registro solicitado, por lo tanto, no se puede eliminar, por favor consulte con el administrador del sitio.'})
    else:
        return redirect('inicio')

# *************************************************************************
# ******************** FUNCTIONS GLOBAL COMPONENTS VUE ********************
# *************************************************************************
def get_diccionario(request, coleccion):
    try:
        info = models.Diccionario.objects.get(coleccion=coleccion)
        return JsonResponse({'status': 'success', 'alias': info.alias, 'campos': info.campos, 'has_data': info.has_data, 'type_head': info.type_head, 'propietario': info.propietario, 'reglas': info.reglas})
    except models.Diccionario.DoesNotExist:
        return JsonResponse({'status': 'failed'})

def basic_import_add(request):
    print('Into basic_import_add')
    periodo = request.POST.get('periodo')
    coleccion = request.POST.get('coleccion')
    print('Coleccion: ' + coleccion)
    type_head = request.POST.get('type_head')
    print('Type_head: ' + type_head)
    delimit = request.POST.get('delimitador')
    print('Delimit: ' + delimit)
    campos = request.POST.get('campos')
    print('Campos: ' + campos)
    codigo = '' if request.POST.get('codigo') == None else request.POST.get('codigo')
    print('Código: ' + codigo)
    campos_list = campos.split('|')
    print('Lista de campos ▼')
    print(campos_list)
    reglas = request.POST.get('reglas')
    print('Reglas: ' + reglas)
    mycodec = request.POST.get('codec')
    print('Codec: ' + mycodec)
    merror = 'strict' if request.POST.get('merror') == None else request.POST.get('merror')
    print('Merror: ' + merror)
    reglas_dict = None if reglas == '' else {x.split(':')[0]: x.split(':')[1] for x in reglas.split('|')}
    imp = models.ControlImportBasic()
    imp.coleccion = coleccion
    imp.campos = '' # campos
    imp.cliente = request.user.cliente
    imp.user = request.user
    imp.clave = codigo
    imp.estado = 'ini'
    imp.save()
    print('Rastreo: ' + str(imp.id))
    mongo = Mongo(coleccion)
    content = None
    result = 0
    campos_str = ''
    rawFile = request.FILES.get("rawfile")
    mensaje = 'none'
    # codecs = ['ascii','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855','cp856','cp857','cp858','cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949','cp950','cp1006','cp1026','cp1125','cp1140','cp1250','cp1251','cp1252','cp1253','cp1254','cp1255','cp1256','cp1257','cp1258','euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext','iso2022_kr','latin_1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6','iso8859_7','iso8859_8','iso8859_9','iso8859_10','iso8859_11','iso8859_13','iso8859_14','iso8859_15','iso8859_16','johab','koi8_r','koi8_t','koi8_u','kz1048','mac_cyrillic','mac_greek','mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004','shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf-8','utf_8_sig']
    # codec = 'utf-8'
    # After dtype param push codec
    # encoding=codec, 
    mnu = 0
    try:
        if type_head == 'auto':
            # content = pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=codec, keep_default_na=False)
            # Las cabeceras no se incluyen en el archivo, deben ser suministradas por campos_list
            with pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=mycodec, encoding_errors=merror, keep_default_na=False, chunksize=40000, low_memory=False) as reader:
                for chunk in reader:
                    if periodo:
                        chunk['crx'] = int(periodo)
                    chunk['ctr'] = imp.id
                    docs = chunk.to_dict(orient='records')
                    result += mongo.insertManyChunk(docs)
                mongo.close()
        elif type_head == 'file_parse':
            # Las cabeceras se incluyen en el archivo, pero se salta la primera línea.
            with pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=mycodec, encoding_errors=merror, keep_default_na=False, chunksize=1000, low_memory=False, skiprows=1) as reader:
                print('Abrió el archivo...')
                print('Chunksize: 1000')
                imp.estado = 'open'
                imp.save()
                for chunk in reader:
                    if periodo:
                        chunk['crx'] = int(periodo)
                    chunk['ctr'] = imp.id
                    docs = chunk.to_dict(orient='records')
                    parcial = mongo.insertManyChunk(docs)
                    result += parcial
                    mnu += 1
                    if mnu % 5 == 0:
                        imp.total = result
                        imp.save()
                    print(f'Chunk: {mnu}, len: {parcial}')
                mongo.close()
        else:   # file_fixed
            # Se salta la primera línea
            with pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=mycodec, encoding_errors=merror, keep_default_na=False, chunksize=40000, low_memory=False, skiprows=1) as reader:
                for chunk in reader:
                    if periodo:
                        chunk['crx'] = int(periodo)
                    chunk['ctr'] = imp.id
                    docs = chunk.to_dict(orient='records')
                    result += mongo.insertManyChunk(docs)
                mongo.close()
            # campos_in_line = content.columns.values.tolist()
            # campos_str = "|".join(campos_in_line)
            # Here block analisys headers type_head
            imp.campos = campos_str
        mensaje = 'success'
    except Exception as e:
        mensaje = str(e)
    
    # # # content['ctr'] = imp.id
    # # # docs = content.to_dict(orient='records')
    # # # result = mongo.insertMany(docs)
    # return JsonResponse({'status': 'success', 'total': result})
    if mensaje == 'success':
        if result > 0:
            imp.total = result
            imp.estado = 'close'
            imp.save()
            return JsonResponse({'status': 'success', 'total': result})
        else:
            imp.delete()
            return JsonResponse({'status': 'failed', 'total': result, 'msn': 'Failed insert many in mongodb.'})
    else:
        imp.estado = 'close'
        imp.save()
        return JsonResponse({'status': 'failed', 'total': result, 'msn': mensaje})

def date_to_string(fl):
    if isinstance(fl, datetime.date):
        return fl.isoformat()

def import_history(request):
    if request.method == 'POST':
        colec = request.POST.get('coleccion')
        print(colec)
        datos = models.ControlImportBasic.objects.filter(coleccion=colec).values('id', 'coleccion', 'created_at', 'total')
        lista = list(datos)
        rs = json.dumps(lista, default=date_to_string)
        return HttpResponse(rs, content_type="application/json")
    else:
        return JsonResponse([], content_type="application/json")

def import_delete_basic(request):
    if request.method == "POST":
        id = request.POST.get('codex')
        coleccion = request.POST.get('coleccion')
        try:
            target = models.ControlImportBasic.objects.get(pk=id)
            if target.coleccion == coleccion:
                mongo = Mongo(coleccion)
                if mongo.removeImport(target.id):
                    target.delete()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'failed', 'msn': 'Falló la eliminación en MongoDB'})
            else:
                return JsonResponse({'status': 'failed', 'msn': 'Las credenciales fallaron'})
        except models.ControlImportBasic.DoesNotExist:
            return JsonResponse({'status': 'failed', 'msn': 'No se encontró la importación referenciada. CTR-' + str(id)})

def getLastImport(request):
    colec = request.POST.get('coleccion')
    # Model.objects.order_by('item_count').last()
    # target = models.ControlImportBasic.objects.filter(coleccion=colec).values('id', 'coleccion', 'created_at', 'total')
    target = models.ControlImportBasic.objects.filter(coleccion=colec).order_by('-created_at').first()  # .values('id', 'coleccion', 'created_at', 'total')
    if target != None:
        return JsonResponse({'status': 'success', 'fecha': target.created_at, 'total': target.total})
    else:
        return JsonResponse({'status': 'empty', 'fecha': None, 'total': 0, 'msn': 'No hay importaciones realizadas.'})

def auto_reader_colection(request):
    if request.method == "POST":
        coleccion = request.POST.get('coleccion')
        calcpages = True if request.POST.get('calcpages') == 'on' else False
        page = int(request.POST.get('pagina')) if request.POST.get('pagina') != None else 1
        if calcpages == True:
            page = 1
        filters = {}
        makles = request.POST.get('makles').split('|') if request.POST.get('makles') != None else []
        for field in makles:
            value = str(request.POST.get(field))
            if value.isnumeric():
                filters[field] = {"$in": [value, int(value)]}
            else:
                filters[field] = value
                
        mongo = Mongo(coleccion)
        result = mongo.findPaginate(filtro=filters, pagina=page, calcular=calcpages)
        return HttpResponse(result, content_type="application/json")
    else:
        coleccion = 'bdua_contributivo_1'
        mongo = Mongo(coleccion)
        result = mongo.findPaginate(calcular=False)
        return HttpResponse(result, content_type="application/json")

def get_ruta(request):
    pass

def getImport(request):
    codigo = request.POST.get('codigo')
    mnu = None
    try:
        imp = models.ControlImportBasic.objects.get(clave=codigo)
        mnu = {'id': imp.id, 'total': imp.total, 'clave': imp.clave, 'estado': imp.estado}
    except models.ControlImportBasic.DoesNotExist:
        mnu = {'id': '', 'total': 0, 'clave': codigo, 'estado': 'void'}
    return JsonResponse(mnu)
    # return HttpResponse(mnu, content_type="application/json")

def ismael(request):
    # with connection.cursor() as cursor:
        # cursor.execute("ALTER TABLE `control_import_basic` ADD `clave` VARCHAR(20) NULL AFTER `total`, ADD `estado` VARCHAR(10) NULL AFTER `clave`;")
        # cursor.execute("SHOW COLUMNS FROM control_import_basic;")
        # row = cursor.fetchall()
        # print(row)
    return render(request, 'users/a_ismael.html')
