from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Hotel_Chain

def index(request):
    hotels = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']
        hotels = Hotel.objects.filter(name__icontains=query)
    else:
        hotels = Hotel.objects.all()
    context = {'hotels' : hotels}
    return render(request, 'booking/hotels.html', context)


def hotel_detail(request, hotel_id=None):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    context = {'hotel' : hotel}
    return render(request, 'booking/hotel_detail.html', context)