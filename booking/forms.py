from django import forms
from .models import Hotel, Image, Room, Room_Type, Booking

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
        fields = ('hotel', 'room_type', 'description', 'price')


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = Room_Type
        fields = ('room_type', 'room_standard', 'smoking_in')


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'description')