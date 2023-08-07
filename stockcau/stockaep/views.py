from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from .forms import *
from .decorators import *
import openpyxl
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django_filters.views import FilterView
from .filters import HardwareFilter

##Funciones

def mayus_minus(pal):
    if pal[-1] == ' ':
        pal[-1].replace(' ', '')
    return pal.lower().capitalize()

# Create your views here.

@login_required(login_url='login')
def index(request):
    ctx = {'link':'index'}
    ctx['data'] = Hardware.objects.all()
    
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
            form.save()
            return redirect('/')
    return render(request, 'main.html', ctx)

@login_required(login_url='login')
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


            if dato[7] == None:
                dato[7] = ''

            hard = Hardware.objects.create(tipo=tipo, marca=marca, modelo=modelo, ubicacion=ubicacion, nro_de_serie=mayus_minus(str(dato[4])), estado=mayus_minus(str(dato[6])), observaciones = mayus_minus(str(dato[7])))
            hard.save()
        
    
    return redirect('index')

@login_required(login_url='login')
def delete(request, id):
    hardware = Hardware.objects.get(id=id)
    hardware.delete()
    return redirect('index')

@login_required(login_url='login')
def edit(request, id):
    to_edit = Hardware.objects.get(id=id)
    ctx = {}
    ctx['to_edit'] = to_edit
    edit_form = HardwareForm(to_edit.toJSON())
    ctx['edit_form'] = edit_form
    if request.method == 'POST':
        to_edit.tipo  = Tipo.objects.get(id=request.POST['tipo'])
        to_edit.marca = Marca.objects.get(id=request.POST['marca'])
        to_edit.modelo = Modelo.objects.get(id=request.POST['modelo'])
        to_edit.nro_de_serie = request.POST['nro_de_serie']
        to_edit.ubicacion = Ubicacion.objects.get(id=request.POST['ubicacion'])
        to_edit.estado = request.POST['estado']
        to_edit.observaciones = request.POST['observaciones']
        to_edit.save()
        return redirect('/')
    return render(request, 'edit_hardware.html', ctx)

def test(request):
    ctx = {
        'link':'test'
    }
    return render(request, 'main.html', ctx)

def get_info(request):
    data = list(Hardware.objects.values())
    
    return JsonResponse(data, safe=False)

class ProductListView(FilterView):
    model = Hardware
    template_name = 'test.html'
    paginate_by = 10
    filterset_class = HardwareFilter