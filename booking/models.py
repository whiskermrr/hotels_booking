from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, URLValidator
from django_countries.fields import CountryField
from django.contrib.auth.models import User



class Hotel_Chain(models.Model):
    chain_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.chain_name


class Hotel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    hotel_chain = models.ForeignKey(Hotel_Chain, blank=True, null=True)
    country_code = CountryField(max_length=100)
    star_rating = models.DecimalField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                      max_digits=3, decimal_places=1)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(max_length=20, validators=[phone_regex])
    address = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='media/avatars', blank=True)
    city = models.CharField(max_length=50)
    url = models.URLField(validators=[URLValidator])

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {}".format(
            self.hotel_chain,
            self.country_code,
            self.star_rating,
            self.name,
            self.email,
            self.phone_number,
            self.address,
            self.city,
            self.url)


class Room_Type(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('twin', 'Twin'),
        ('triple', 'Triple'),
        ('multiple', 'Multiple')
    )
    room_type = models.CharField(choices=ROOM_TYPES, max_length=10)
    room_standard = models.CharField(max_length=100)
    smoking_in = models.BooleanField()

    def __str__(self):
        return "{} {}".format(self.room_type, self.room_standard)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(Room_Type, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    avatar = models.ImageField(upload_to='media/images', blank=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return "{} {}".format(self.price.__str__(), self.room_type.__str__())


class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True)
    room =  models.ForeignKey(Room, on_delete=models.CASCADE, blank=True)
    start_date = models.DateField(auto_now=False, auto_created=False)
    end_date = models.DateField(auto_now=False, auto_created=False)
    booked_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return "%s %s %s %s %s %s" % (
            self.description,
            self.guest.__str__(),
            self.hotel.__str__(),
            self.room.__str__(),
            self.start_date,
            self.end_date,
        )


class Payment(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.amount.__str__(), self.status.__str__(), self.date)


class Image(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='media/images')


class Rating(models.Model):
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return "{} {}".format(self.rate.__str__(), self.hotel.__str__())


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, blank=True)
    context = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.user.__str__(), self.context.__str__(), self.date)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='receiver')
    content = models.CharField(max_length=500)

    def __str__(self):
        return "{} {} {}".format(self.sender.__str__(), self.receiver.__str__(), self.content)