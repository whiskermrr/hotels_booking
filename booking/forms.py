from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'address', 'email', 'phone_number')