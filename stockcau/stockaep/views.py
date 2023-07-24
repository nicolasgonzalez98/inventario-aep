from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
import openpyxl
# Create your views here.

def index(request):
    df = openpyxl.load_workbook("Inventario.xlsx")
    dataframe = df.active
    data = []

    for row in range(1, dataframe.max_row):
        _row=[row]
        for col in dataframe.iter_cols(1,dataframe.max_column):
            _row.append(col[row].value)
        data.append(_row)
    
    print(data[0])

    for dato in data:
        print(data[0][0])
        tipo, create = Tipo.objects.get_or_create(name = dato[1])
        print(tipo)
        marca, create = Marca.objects.get_or_create(nombre = dato[2])
        print(marca)
        modelo, create = Modelo.objects.get_or_create(nombre = dato[3], marca = marca)
        print(modelo)
        ubicacion, create = Ubicacion.objects.get_or_create(nombre=dato[5])
        print(ubicacion)
        
    

    return render(request, 'main.html')

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