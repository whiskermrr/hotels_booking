from django.forms import modelformset_factory
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *

def hotels(request):
    hotels = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']
        hotels = Hotel.objects.filter(Q(name__icontains=query) |
                                      Q(city__icontains=query) |
                                      Q(country_code__icontains=query)
                                      )
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



def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    images = Image.objects.filter(room=room_id)
    image = images[0]
    comments_list = Comment.objects.filter(room=room_id).order_by('-date')
    paginator = Paginator(comments_list, 5)
    page_var = 'page'
    page = request.GET.get(page_var)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'room': room,
        'image': image,
        'comments': comments,
        'page_var': page_var,
    }
    if request.method == 'POST':
        return comment_add(request, room_id)

    return render(request, 'booking/room_detail.html', context)


def comment_add(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        commentForm = CommentForm()
        comment_form = commentForm.save(commit=False)
        comment_form.user = request.user
        comment_form.room = room
        comment_form.context = request.POST.get('content')

        ratingForm = RatingForm()
        rating_form = ratingForm.save(commit=False)
        rating_form.rate = request.POST.get('rating')
        rating_form.hotel = room.hotel
        rating_form.save()
        comment_form.rating = rating_form
        comment_form.save()

    return redirect('booking:room_detail', room.id)



def room_type_add(request):
    if request.method == 'POST':
        room_type_form = RoomTypeForm(request.POST)
        if room_type_form.is_valid():
            room_type_form.save(commit=False)
            room_type_form.save()

            return render(request, 'booking/index.html', {})

    else:
        room_type_form = RoomTypeForm()
        return render(request, 'booking/room_type_add.html', {'roomTypeForm' : room_type_form})


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



def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'booking/user_profile.html', {'user' : user})


def room_bookit(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    hotel = get_object_or_404(Hotel, id=room.hotel.id)

    if request.user.is_authenticated():
        if request.method == 'POST':
            bookingForm = BookingForm(request.POST)
            if bookingForm.is_valid():
                booking_form = bookingForm.save(commit=False)
                #date validations goes here
                if booking_form.start_date >= booking_form.end_date:
                    return clear_booking_form(request, 'Wrong dates!', hotel, room)

                bookings = Booking.objects.filter(room=room)

                for booking in bookings:
                    if booking.start_date <= booking_form.start_date < booking.end_date or booking.start_date < booking_form.end_date <= booking.end_date:
                        return clear_booking_form(request, 'Room is already booked for this dates!', hotel, room)

                #days = booking_form.end_date.day - booking_form.start_date.day
                #price = days * room.price
                booking_form.guest = request.user
                booking_form.room = room
                booking_form.hotel = hotel
                booking_form.save()
                #return render(request, 'booking/room_bookit_confirm.html', {'booking': booking_form, 'price': price })
                return redirect('booking:booking_confirm', booking_id=booking_form.id)

            else:
                return clear_booking_form(request, 'Invalid form!', hotel, room)

        else:
            return clear_booking_form(request, 'Almost done!', hotel, room)

    else:
        return redirect('auth_login')


def clear_booking_form(request, title, hotel, room):
    title = title
    bookingForm = BookingForm(initial={'hotel': hotel.id})
    context = {
        'bookingForm': bookingForm,
        'title': title,
        'hotel': hotel,
        'room': room,
    }
    return render(request, 'booking/room_bookit.html', context)



def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user.is_authenticated() and request.user.id == booking.guest.id:
        if booking:
            days = booking.end_date.day - booking.start_date.day
            price = days * booking.room.price
            if request.method == 'POST':
                paymentForm = PaymentForm()
                payment_form = paymentForm.save(commit=False)
                payment_form.guest = booking.guest
                payment_form.booking = booking
                payment_form.amount = price
                payment_form.status = False
                payment_form.save()
                return redirect('booking:user_bookings', username=request.user)
            else:
                return render(request, 'booking/room_bookit_confirm.html', {'booking': booking, 'price': price})

    else:
        return redirect('auth_login')


def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('booking:index')



def user_bookings(request, username):
    bookings = Booking.objects.filter(guest_id=request.user.id)
    return render(request, 'booking/user_bookings.html', {'bookings': bookings})


def user_payments(request, username):
    payments = Payment.objects.filter(guest_id=request.user.id)
    return render(request, 'booking/user_payments.html', {'payments': payments})


def pay_bill(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if payment:
        payment.status = True
        print('STATUS CHANGED!')
        payment.save()

    return redirect('booking:user_payments', username=request.user)


def hotel_chain_add(request):
    if request.method == 'POST':
        hotelChainForm = HotelChainForm(request.POST)
        if hotelChainForm.is_valid():
            hotel_chain_form = hotelChainForm.save(commit=False)
            hotel_chain_form.save()
            return redirect('booking:index')

    else:
        hotelChainForm = HotelChainForm()
        return render(request, 'booking/hotel_chain_add.html', {'hotelChainForm': hotelChainForm})