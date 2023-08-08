from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.contrib.auth.models import Group

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

class Hardware(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    nro_de_serie = models.CharField(max_length=100, null=False, default='', unique=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, default='1', choices=ESTADOS_HARDWARE)
    observaciones = models.TextField(max_length=500, default='')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.tipo}'
    
    class Meta:
        ordering = ['tipo']

# class Contador(models.Model):
#     tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
#     cantidad = models.IntegerField(default=0)