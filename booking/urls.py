from django.conf.urls import url
from . import views


app_name = 'booking'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hotels$', views.hotels, name='hotels'),
    url(r'^(?P<hotel_id>[0-9]+)/$', views.hotel_detail, name='hotel_detail'),
    url(r'^rooms/(?P<room_id>[0-9]+)/$', views.room_detail, name='room_detail'),
    url(r'^rooms/(?P<room_id>[0-9]+)/bookit$', views.room_bookit, name='room_bookit'),
    url(r'^bookings/(?P<booking_id>[0-9]+)/confirm/$', views.booking_confirm, name='booking_confirm'),
    url(r'^bookings/(?P<booking_id>[0-9]+)/cancel/$', views.booking_cancel, name='booking_cancel'),
    #url(r'^register$', views.register, name='register'),
    url(r'^hotels/add$', views.hotel_add, name='hotel_add'),
    url(r'^rooms/add$', views.room_add, name='room_add'),
    url(r'^room_types/add$', views.room_type_add, name='room_type_add'),
    url(r'^users/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^users/(?P<username>\w+)/bookings$', views.user_bookings, name='user_bookings'),
    url(r'^users/(?P<username>\w+)/payments', views.user_payments, name='user_payments'),
    url(r'^payments/(?P<payment_id>[0-9]+)/$', views.pay_bill, name='pay_bill'),
    url(r'^hotel_chains/add$', views.hotel_chain_add, name='hotel_chain_add'),
]