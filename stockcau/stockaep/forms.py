from django.forms import ModelForm
from .models import * 

class HardwareForm(ModelForm):
    def __init__(self, *args, **kwargs):
         super(HardwareForm, self).__init__(*args, **kwargs) 
         self.fields['marca'].widget.attrs = {
            'id':'marca',
            'class':'form-control',
        }
    class Meta:
        model = Hardware
        fields=["marca"]