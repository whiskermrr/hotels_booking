from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'address', 'email', 'phone_number')


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('hotel_chain', 'country_code', 'name', 'email', 'address', 'city', 'email', 'phone_number', 'url')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('image', )