from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from .forms import *
import openpyxl

##Funciones

def mayus_minus(pal):
    if pal[-1] == ' ':
        pal[-1].replace(' ', '')
    return pal.lower().capitalize()

# Create your views here.

def index(request):
    ctx = {'link':'index'}
    form_edit = HardwareForm()
    ctx['data'] = Hardware.objects.all()
    ctx['marcas'] = Marca.objects.all()
    for i in ctx['marcas']:
        print(i.nombre)
    #ctx['form_edit'] = form_edit
    ##print(form_edit)
    return render(request, 'main.html', ctx)

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

                user_model = User.objects.get(username=username)
                nuevo_tecnico = Tecnico.objects.create(user = user_model, id_user = user_model.id, nombre=name, apellido = surname)
                nuevo_tecnico.save()
                return redirect('login')
        else:
            messages.info(request, 'Las contraseñas no coinciden.')
            return redirect('register') 
    return render(request,'signup.html')

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

def logout(request):
    auth.logout(request)
    return redirect('login')

def add_inventary(request):
    form_add_inventary = HardwareForm()
    ctx = {'link':'create'}
    ctx['form_add_inventary'] = form_add_inventary
    return render(request, 'main.html', ctx)

def reload(request):
    df = openpyxl.load_workbook("Inventario.xlsx")
    dataframe = df.active
    data = []
    ctx = {'link':'index'}

    for row in range(1, dataframe.max_row):
        _row=[row]
        for col in dataframe.iter_cols(1,dataframe.max_column):
            _row.append(col[row].value)
        data.append(_row)
    
    

    for dato in data:
        
            print(data)
            tipo, create = Tipo.objects.get_or_create(name = mayus_minus(str(dato[1])))
            marca, create = Marca.objects.get_or_create(nombre = mayus_minus(str(dato[2]))) 
            modelo, create = Modelo.objects.get_or_create(nombre = mayus_minus(str(dato[3])), marca = marca)
            ubicacion, create = Ubicacion.objects.get_or_create(nombre=mayus_minus(str(dato[5])))


            hard = Hardware.objects.create(tipo=tipo, marca=marca, modelo=modelo, ubicacion=ubicacion, nro_de_serie=mayus_minus(str(dato[4])), estado=mayus_minus(str(dato[6])), observaciones = mayus_minus(str(dato[7])))
            hard.save()
        
    
    return redirect('index')

def delete(request, id):
    hardware = Hardware.objects.get(id=id)
    hardware.delete()
    return redirect('index')

