from django.conf.urls import url
from . import views


app_name = 'booking'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hotels$', views.hotels, name='hotels'),
    url(r'^(?P<hotel_id>[0-9]+)/$', views.hotel_detail, name='hotel_detail'),
    #url(r'^register$', views.register, name='register'),
    url(r'^hotels/add$', views.hotel_add, name='hotel_add'),
    url(r'^rooms/add$', views.room_add, name='room_add'),
    url(r'^users/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
]