import django_filters

from .models import Hardware


class HardwareFilter(django_filters.FilterSet):

    class Meta:
        model = Hardware
        fields = ['nro_de_serie']