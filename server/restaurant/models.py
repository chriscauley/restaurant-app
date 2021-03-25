from django.conf import settings
from django.db import models


def serialize(obj, attrs):
    return { attr: getattr(obj, attr) for attr in attrs }


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Restaurant(BaseModel):
    class Meta:
        ordering = ('-created',)
    name = models.CharField(max_length=256)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    photo = models.ImageField(upload_to="restaurant_photos", null=True, blank=True)
    __str__ = lambda self: self.name
    @property
    def photo_url(self):
        if not self.photo:
            return None
        return self.photo.url
    def user_can_edit(self, user):
        return user == self.owner
    def get_json(self, user):
        data = serialize(self, ['id', 'name', 'description', 'photo_url'])
        menusections = self.menusection_set.all().prefetch_related('menuitem_set')
        data['menusections'] = [s.get_json(user) for s in menusections]
        data['is_owner'] = self.user_can_edit(user)
        data['is_blocked'] = OwnerBlock.objects.filter(owner=self.owner, user_id=user.id).exists()
        return data


class MenuSection(BaseModel):
    class Meta:
        ordering = ('-created',)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)
    name = models.CharField(max_length=256)
    __str__ = lambda self: self.name

    def get_json(self, user):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.get_json(user) for item in self.menuitem_set.all()]
        }


class MenuItem(BaseModel):
    menusection = models.ForeignKey(MenuSection, models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    __str__ = lambda self: self.name
    def get_json(self, user):
        return serialize(self, ['id', 'name', 'price', 'description'])
    class Meta:
        ordering = ('-created',)


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
    total_items = models.IntegerField(default=0)
    total_price = models.DecimalField(default=0,max_digits=6, decimal_places=2)

    @property
    def user_name(self):
        return self.user.username

    @property
    def user_avatar_url(self):
        return self.user.avatar_url

    @property
    def restaurant_name(self):
        return self.restaurant.name

    @property
    def restaurant_photo_url(self):
        return self.restaurant.photo_url

    @property
    def items(self):
        attrs = ['quantity', 'name', 'price', 'id']
        return [serialize(item, attrs) for item in self.orderitem_set.all()]

    @property
    def status_history(self):
        status_times = {}
        for update in self.orderstatusupdate_set.all().order_by('created'):
            status_times[update.status] = update.created
        choices = self._status_choices[:]
        if self.status == 'canceled':
            choices.remove('received')
        else:
            choices.remove('canceled')
        return [{ 'status': s, 'created': status_times.get(s) } for s in choices]

    def set_status(self, status):
        self.status = status
        self.save()
        OrderStatusUpdate.objects.create(order=self, status=status)

    def user_can_see_order(self, user):
        return user.is_superuser or user.id == self.user_id or self.is_restaurant_owner(user)

    def is_restaurant_owner(self, user):
        return self.restaurant.user_can_edit(user)

    def get_allowed_status(self, user):
        if self.status in ['canceled', 'received']:
            return
        for new_status in self._status_choices:
            if self.user_can_set_status(user, new_status):
                return new_status

    def user_can_set_status(self, user, new_status):
        if user.id == self.user_id:
            if self.status == 'placed':
                return new_status == 'canceled'
            if self.status == 'delivered':
                return new_status == 'received'
        elif self.is_restaurant_owner(user):
            if self.status == 'placed':
                return new_status == 'processing'
            if self.status == 'processing':
                return new_status == 'in_route'
            if self.status == 'in_route':
                return new_status == 'delivered'
        # anything else is not allowed

    class Meta:
        ordering = ('-created',)

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
    class Meta:
        ordering = ('-created',)


class OrderStatusUpdate(BaseModel):
    order = models.ForeignKey(Order, models.CASCADE)
    status = models.CharField(max_length=16, choices=Order.STATUS_CHOICES)
    class Meta:
        ordering = ('-created',)


class OwnerBlock(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='+')
