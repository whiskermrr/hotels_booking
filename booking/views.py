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
    context = {
        'hotel' : hotel,
        'rooms' : rooms
    }
    return render(request, 'booking/hotel_detail.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('booking:index')
    else:
        user_form = UserForm()
        return render(request, 'booking/register.html', {'user_form' : user_form})
