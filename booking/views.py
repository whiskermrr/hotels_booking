from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
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

            hotels = Hotel.objects.all()
            return render(request, 'booking/hotels.html', {'hotels' : hotels})

        else:
            print (hotelForm.errors, formset.errors)

    else:
        hotelForm = HotelForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        context = {'hotelForm' : hotelForm, 'formset' : formset}
        return render(request, 'booking/hotel_add.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('booking:index')
    else:
        user_form = UserForm()
        return render(request, 'booking/register.html', {'user_form' : user_form})
