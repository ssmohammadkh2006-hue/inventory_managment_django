from django import forms 
from.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        
class DistributorsForm(forms.ModelForm):
    class Meta:
        model=Distributor 
        fields="__all__"
        
class SalesForm(forms.ModelForm):
    class Meta:
        model=Sale
        fields="__all__"