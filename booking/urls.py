from django.conf.urls import url
from . import views


app_name = 'booking'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'hotel/?(P<hotel_id>[0-9]+)', views.hotel_detail, name='hotel_detail'),

]