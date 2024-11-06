# forms.py
from django import forms
from db.models import *

class WorkzoneForm(forms.ModelForm):
    class Meta:
        model = Workzone
        fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'country']

