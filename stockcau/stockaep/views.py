from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from .forms import *
from .decorators import *
import openpyxl
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .filters import HardwareFilter
from django_filters.views import FilterView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

PRODUCTS_PER_PAGE = 25

##Funciones

def mayus_minus(pal):
    pal.strip()
    if pal[-1] == ' ':
        pal.replace(' ', '')
    return pal.lower().capitalize()

# Create your views here.

@login_required(login_url='login')
def index(request):
    
    page = request.GET.get('page',1)
    
    f = HardwareFilter(request.GET, queryset=Hardware.objects.all())
    
    product_paginator = Paginator(list(f.qs), PRODUCTS_PER_PAGE)
    
    try:
        pagina = product_paginator.page(page)
    except EmptyPage:
        pagina = product_paginator.page(product_paginator.num_pages)
    except:
        pagina = product_paginator.page(product_paginator.num_pages)
    ctx = {
        'link':'index',
        'filter':f,
        'pagina': pagina,
        'paginator':product_paginator,
        'cant_pags':product_paginator.page_range
    }
    
    return render(request, 'main.html', ctx)

@unauthorized_user
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        name = request.POST['name']
        surname = request.POST['surname']
        
        

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email ya usado')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                group, create=Group.objects.get_or_create(name='user')
                user_model = User.objects.get(username=username)
                user_model.groups.add(group)
                nuevo_tecnico = Tecnico.objects.create(user = user_model, id_user = user_model.id, nombre=name, apellido = surname)
                nuevo_tecnico.save()
                return redirect('login')
        else:
            messages.info(request, 'Las contraseñas no coinciden.')
            return redirect('register') 
    return render(request,'signup.html')

@unauthorized_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        

        user = auth.authenticate(username=username, password=password)
        

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Credentials invalid')
            return redirect('login')
    return render(request, 'signin.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_inventary(request):
    form_add_inventary = HardwareForm()
    
    ctx = {'link':'create'}
    ctx['form_add_inventary'] = form_add_inventary

    if request.method == 'POST':
        form = HardwareForm(request.POST)
        if form.is_valid():
            tipo, create = Tipo.objects.get_or_create(id = request.POST['tipo'])
            marca, create = Marca.objects.get_or_create(id = request.POST['marca']) 
            modelo = Modelo.objects.get(id = request.POST['modelo'])
            ubicacion, create = Ubicacion.objects.get_or_create(id=request.POST['ubicacion'])
            estado, create = Estado.objects.get_or_create(id = request.POST['estado'])
            
            hardware = Hardware.objects.create(tipo = tipo, marca=marca, modelo=modelo,ubicacion=ubicacion, estado = estado, nro_de_serie=request.POST['nro_de_serie'], observaciones = request.POST['observaciones'])
            
            if(request.user.is_staff == False):
                Notificacion.objects.create(hardware=hardware, usuario = request.user, tipo = 'CREATE')
            
            return redirect('/')
    return render(request, 'main.html', ctx)

@login_required(login_url='login')
@admin_only
def reload(request):
    df = openpyxl.load_workbook("Inventario.xlsx")

    
    dataframe = df.active
    data = []
    

    for row in range(1, dataframe.max_row):
        _row=[row]
        for col in dataframe.iter_cols(1,dataframe.max_column):
            _row.append(col[row].value)
        data.append(_row)

    for dato in data:
            tipo, create = Tipo.objects.get_or_create(name = mayus_minus(str(dato[1])))
            marca, create = Marca.objects.get_or_create(nombre = mayus_minus(str(dato[2]))) 
            modelo, create = Modelo.objects.get_or_create(nombre = mayus_minus(str(dato[3])), marca = marca)
            ubicacion, create = Ubicacion.objects.get_or_create(nombre=mayus_minus(str(dato[5])))
            estado, create = Estado.objects.get_or_create(nombre = 'Activo')

            if dato[7] == None:
                dato[7] = ''
            else:
                dato[7] = mayus_minus(str(dato[7]))

            hard = Hardware.objects.create(tipo=tipo, marca=marca, modelo=modelo, ubicacion=ubicacion, estado = estado, nro_de_serie=mayus_minus(str(dato[4])).upper(), observaciones = dato[7])
            hard.save()

    df = openpyxl.load_workbook("inventariot4.xlsx")
    
    for i in df.sheetnames:
        dataframe = df[i]
        data = []

        for row in range(1, dataframe.max_row):
            _row=[row]
            for col in dataframe.iter_cols(1,dataframe.max_column):
                _row.append(col[row].value)
            data.append(_row)

        for dato in data:
            tipo, create = Tipo.objects.get_or_create(name = mayus_minus(str(dato[1])))
            marca, create = Marca.objects.get_or_create(nombre = mayus_minus(str(dato[2]))) 
            modelo, create = Modelo.objects.get_or_create(nombre = mayus_minus(str(dato[3])), marca = marca)
            ubicacion, create = Ubicacion.objects.get_or_create(nombre=mayus_minus(str(dato[6])))
            estado, create = Estado.objects.get_or_create(nombre = 'Activo')

            if dato[7] == None:
                dato[7] = ''
            else:
                if len(dato) > 8:
                    print(dato[8])
                    dato[7] = mayus_minus(str(dato[7]))
                else:
                    dato[7] = mayus_minus(str(dato[7]))
            hard = Hardware.objects.create(tipo=tipo, marca=marca, modelo=modelo, ubicacion=ubicacion, estado = estado, nro_de_serie=mayus_minus(str(dato[4])).upper(), observaciones = dato[7])
            hard.save()
    
    return redirect('index')

@login_required(login_url='login')
def delete(request, id):
    if(request.user.is_staff):
        hardware = Hardware.objects.get(id=id)
        hardware.delete()
        return redirect('index')
    else:
        hardware = Hardware.objects.get(id=id)
        usuario = User.objects.get(username = request.user)
        Notificacion.objects.create(hardware=hardware, usuario = usuario, tipo = 'DELETE')
        return redirect('index')

@login_required(login_url='login')
def edit(request, id):
    to_edit = Hardware.objects.get(id=id)
    ctx = {}
    ctx['to_edit'] = to_edit
    edit_form = HardwareForm(to_edit.toJSON())
    ctx['edit_form'] = edit_form
    ctx['link'] = 'edit'
    
    
    if request.method == 'POST':
        
        to_edit.tipo  = Tipo.objects.get(id=request.POST['tipo'])
        to_edit.marca = Marca.objects.get(id=request.POST['marca'])
        to_edit.modelo = Modelo.objects.get(id=request.POST['modelo'])
        to_edit.ubicacion = Ubicacion.objects.get(id=request.POST['ubicacion'])
        to_edit.observaciones = request.POST['observaciones']
        if(request.user.is_staff):
            to_edit.nro_de_serie = request.POST['nro_de_serie']
            to_edit.estado = Estado.objects.get(id=request.POST['estado'])
        else:
            nro_serie = ''
            estado = ''
            if to_edit.nro_de_serie != request.POST['nro_de_serie']:
                nro_serie= request.POST['nro_de_serie']
            if to_edit.estado != Estado.objects.get(id=request.POST['estado']):
                estado= (Estado.objects.get(id=request.POST['estado'])).nombre
    
            Notificacion.objects.create(hardware=to_edit, usuario = User.objects.get(username = request.user), tipo = 'EDIT', nro_de_serie = nro_serie, estado = estado)
        to_edit.save()
        
        return redirect('/')
    
    return render(request, 'main.html', ctx)

# def test(request):
#     page = request.GET.get('page',1)
    
#     f = HardwareFilter(request.GET, queryset=Hardware.objects.all())
#     product_paginator = Paginator(list(f.qs), PRODUCTS_PER_PAGE)
#     try:
#         pagina = product_paginator.page(page)
#     except EmptyPage:
#         print('hola')
#         pagina = product_paginator.page('1')
#     ctx = {
#         'link':'test',
#         'filter':f,
#         'pagina': pagina,
#         'paginator':product_paginator
#     }
#     return render(request, 'main.html', ctx)

def get_info(request):
    data = list(Hardware.objects.values())
    
    return JsonResponse(data, safe=False)

@login_required(login_url='login')
@admin_only
def notificaciones(request):
    ctx={'link':'notification'}

    notificaciones = Notificacion.objects.filter(realizado = False)
    
    ctx['notificaciones'] = notificaciones
    ctx['cant_notificaciones'] = len(notificaciones)
    return render(request, 'main.html', ctx)

@login_required(login_url='login')
@admin_only
def accion_notificacion(request):
    id = request.GET.get('id')
    status = request.GET.get('status')
    notificacion = Notificacion.objects.get(id=id)

    
    if (notificacion.tipo == 'CREATE' and status == 'cancel') or (notificacion.tipo == 'DELETE' and status == 'accept'):
        hardware = Hardware.objects.get(id = notificacion.hardware.id)
        hardware.delete()
    elif(notificacion.tipo == 'EDIT' and status == 'accept'):
        hardware = Hardware.objects.get(id = notificacion.hardware.id)
        if notificacion.nro_de_serie:
            hardware.nro_de_serie = notificacion.nro_de_serie
        if notificacion.estado:
            hardware.estado = Estado.objects.get(nombre = notificacion.estado)
        hardware.save()

    notificacion.realizado = True
    notificacion.save()

    return redirect(reverse('notifications') + f'?item={id}')

def asignacion(request):
    id = request.GET.get('id')
    hardware = Hardware.objects.get(id=id)
    if request.method == 'POST':
        person = request.POST['person']
        if len(person) == 0:
            return redirect('index')
        Asignacion.objects.create(hardware=hardware, usuario=person)
        return redirect('index')
    
    return redirect('index')


