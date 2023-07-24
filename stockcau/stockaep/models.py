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