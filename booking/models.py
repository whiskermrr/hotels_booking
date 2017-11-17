from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, URLValidator
from django_countries.fields import CountryField
from smart_selects.db_fields import ChainedForeignKey


class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(max_length=20, validators=[phone_regex])

    def __str__(self):
        return "%s %s %s %s %s" % (self.name, self.surname, self.address, self.email, self.phone_number)


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class Hotel_Chain(models.Model):
    chain_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.chain_name


class Hotel(models.Model):
    hotel_chain = models.ForeignKey(Hotel_Chain, blank=True, null=True)
    country_code = CountryField(max_length=100)
    star_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(max_length=20, validators=[phone_regex])
    address = models.CharField(max_length=100)
    """city = ChainedForeignKey(
        Country_Code,
        chained_field="country_code",
        chained_model_field="country_code",
        show_all=False,
        sort=True,
        auto_choose=True)"""
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
    description = models.CharField(max_length=100)

    def __str__(self):
        return "{} {} {}".format(self.room_type, self.room_standard, self.description)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(Room_Type, on_delete=models.CASCADE)
    smoking_in = models.BooleanField()

    def __str__(self):
        return "{} {}".format(self.room_type.__str__(), self.smoking_in)


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_mrr')
    room = ChainedForeignKey(
        Room,
        chained_field="hotel",
        chained_model_field="hotel",
        show_all=False,
        sort=True,
        auto_choose=True
    )
    start_date = models.DateField(auto_now=False, auto_created=False)
    end_date = models.DateField(auto_now=False, auto_created=False)
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
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField(auto_now_add=True)