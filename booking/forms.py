from django import forms
from .models import Hotel, Image, Room

"""
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'address', 'email', 'phone_number')
"""

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('hotel_chain', 'country_code', 'name', 'email', 'address', 'city', 'email', 'phone_number', 'star_rating', 'url')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('image', )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('hotel', 'room_type', 'smoking_in')