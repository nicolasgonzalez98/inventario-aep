import django_filters
from django.db import models
from django import forms

from .models import Hardware


class HardwareFilter(django_filters.FilterSet):

    class Meta:
        model = Hardware
        fields = ['nro_de_serie', 'tipo', 'marca', 'modelo']
        filter_overrides = {
             models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                     'widget': forms.TextInput(attrs={'class': 'form-control'})
                 },
             }
        }