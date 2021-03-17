from django.conf import settings
from django.db import models


def serialize(obj, attrs):
    return { attr: getattr(obj, attr) for attr in attrs }


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
    _status_choices = [
        'placed',
        'canceled',
        'processing',
        'in_route',
        'delivered',
        'received'
    ]
    STATUS_CHOICES = zip(_status_choices, _status_choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    @property
    def user_name(self):
        return self.user.username
    @property
    def restaurant_name(self):
        return self.restaurant.name
    @property
    def items(self):
        attrs = ['quantity', 'name', 'price', 'id']
        return [serialize(item, attrs) for item in self.orderitem_set.all()]
    @property
    def status_history(self):
        return [serialize(osu, ['status', 'created']) for osu in self.orderstatusupdate_set.all()]
    def set_status(self, status):
        self.status = status
        self.save()
        OrderStatusUpdate.objects.create(order=self, status=status)
    def user_can_see_order(self, user):
        return user.is_superuser or user.id == self.user_id or self.is_restaurant_owner(user)
    def is_restaurant_owner(self, user):
        return user in self.restaurant.owners.all()
    def get_allowed_statuses(self, user):
        return [status for status in self._status_choices if self.user_can_set_status(user, status)]
    def user_can_set_status(self, user, status):
        if status == 'canceled':
            return user == self.user and self.status == 'placed'
        if status == 'received':
            return user == self.user and self.status == 'delivered'
        if status == 'processing':
            return self.is_restaurant_owner(user) and self.status == 'placed'
        if status == 'in_route':
            return self.is_restaurant_owner(user) and self.status == 'processing'
        if status == 'delivered':
            return self.is_restaurant_owner(user) and self.status == 'in_route'
        # anything else is not allowed


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, models.CASCADE)
    quantity = models.IntegerField()
    @property
    def name(self):
        return self.menuitem.name
    @property
    def price(self):
        return self.menuitem.price


class OrderStatusUpdate(BaseModel):
    order = models.ForeignKey(Order, models.CASCADE)
    status = models.CharField(max_length=16, choices=Order.STATUS_CHOICES)
