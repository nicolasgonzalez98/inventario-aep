from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Tecnico(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    id_user = models.IntegerField()

class Tipo(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.name

class Marca(models.Model):
    nombre = models.CharField(max_length=50, null=False, default='S/D', unique=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=100, null=False, default='S/D', unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class Hardware(models.Model):
    tipo = models.OneToOneField(Tipo, on_delete=models.CASCADE)
    marca = models.OneToOneField(Marca, on_delete=models.CASCADE, default=1)
    modelo = models.OneToOneField(Modelo, on_delete=models.CASCADE, default=1)
    nro_de_serie = models.CharField(max_length=100, null=False, unique=True, default='S/D')
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE, default=1)
    estado = models.CharField(max_length=100, default='')
    observaciones = models.TextField(max_length=500, default='')

    def __str__(self):
        return f'{self.tipo}'
