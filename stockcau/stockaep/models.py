from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.contrib.auth.models import Group
import time

# Create your models here.

##Opciones

ESTADOS_HARDWARE = (
    ('1', 'Activo'),
    ('2', 'En uso'),
    ('3', 'Fuera de Servicio'),
    ('4', 'Scrap'),
    ('5', 'RMA')
)

User = get_user_model()

class Tecnico(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    id_user = models.IntegerField()

class Tipo(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name

class Marca(models.Model):
    nombre = models.CharField(max_length=50, null=False, default='S/D', unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=100, null=False, default='S/D')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre
    
    

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Estado(models.Model):
    estados_hardware = (
    ('Activo', 'Activo'),
    ('En uso', 'En uso'),
    ('Fuera de Servicio', 'Fuera de Servicio'),
    ('Scrap', 'Scrap'),
    ('Scrap', 'RMA')
)
    nombre = models.CharField(choices=estados_hardware, max_length=50)

    def __str__(self):
        return f'{self.nombre}'

class Hardware(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    nro_de_serie = models.CharField(max_length=100, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=500, blank=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    

    def __str__(self):
        return f'{self.tipo}'
    
    class Meta:
        ordering = ['tipo']

class Contador(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    cantidad = models.IntegerField(default=0)

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Notificacion(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, db_constraint=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    realizado = models.BooleanField(default=False)
    tipo = models.CharField(max_length=20)
    estado = models.CharField(max_length=50)
    nro_de_serie = models.CharField(max_length=100)

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Asignacion(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.DO_NOTHING)
    usuario = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nro_ticket = models.CharField(blank=True, max_length=10)
    nota = models.TextField(blank=True, max_length=200)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    