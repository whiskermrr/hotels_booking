from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import *

def hotels(request):
    hotels = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']
        hotels = Hotel.objects.filter(name__icontains=query)
    else:
        hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'booking/hotels.html', context)



def index(request):
    return render(request, 'booking/index.html', {})



def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel_id)
    images = Image.objects.filter(hotel=hotel_id)
    image = images[0]
    context = {
        'hotel' : hotel,
        'rooms' : rooms,
        'image' : image,
    }
    return render(request, 'booking/hotel_detail.html', context)


def hotel_add(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)

    if request.method == 'POST':
        hotelForm = HotelForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if hotelForm.is_valid() and formset.is_valid():
            hotel_form = hotelForm.save(commit=False)
            hotel_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Image(hotel=hotel_form, image=image)
                photo.save()

            image = formset.cleaned_data[0]['image']
            hotel_form.avatar = image
            hotel_form.save()

            hotels = Hotel.objects.all()
            return render(request, 'booking/hotels.html', {'hotels' : hotels})

        else:
            print (hotelForm.errors, formset.errors)

    else:
        hotelForm = HotelForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        context = {'hotelForm' : hotelForm, 'formset' : formset}
        return render(request, 'booking/hotel_add.html', context)



def room_add(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)

    if request.method == 'POST':
        roomForm = RoomForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if roomForm.is_valid() and formset.is_valid():
            room_form = roomForm.save(commit=False)
            room_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Image(room=room_form, image=image)
                photo.save()

            image = formset.cleaned_data[0]['image']
            room_form.avatar = image
            room_form.save()

            return render(request, 'booking/index.html', {})

        else:
            print (roomForm.errors, formset.errors)

    else:
        roomForm = RoomForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        context = {'roomForm' : roomForm, 'formset' : formset}
        return render(request, 'booking/room_add.html', context)
"""
def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('booking:index')
    else:
        user_form = UserForm()
        return render(request, 'booking/register.html', {'user_form' : user_form})
"""

def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'booking/user_profile.html', {'user' : user})

