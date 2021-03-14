from django.conf import settings
from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to="restaurant_photos", null=True, blank=True)
    __str__ = lambda self: self.name
    @property
    def photo_url(self):
        if not self.photo:
            return None
        return self.photo.url
    @property
    def owner_ids(self):
        return [o.id for o in self.owners.all()]


class MenuSection(BaseModel):
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)
    name = models.CharField(max_length=256)
    __str__ = lambda self: self.name


class MenuItem(BaseModel):
    menusection = models.ForeignKey(MenuSection, models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    __str__ = lambda self: self.name


class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, models.CASCADE)
    quantity = models.IntegerField(default=0)


class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)
    _status_choices = [
        'placed',
        'canceled',
        'processing',
        'in_route',
        'delivered',
        'received'
    ]
    STATUS_CHOICES = zip(_status_choices, _status_choices)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, models.CASCADE)
    quantity = models.IntegerField()
