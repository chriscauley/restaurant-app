from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from server.decorators import user_role_required
from server.restaurant.models import Restaurant, Order, MenuSection, MenuItem, Cart, CartItem, serialize, OwnerBlock
from unrest.pagination import paginate

def restaurant_list(request):
    query = Restaurant.objects.all()
    if request.user.is_authenticated and request.user.role == 'owner':
        # owners only see restaurants they control
        query = query.filter(owner=request.user)
    else:
        # non-owners cannot see blocked restaurants
        blocks = OwnerBlock.objects.filter(user=request.user).values_list('owner_id', flat=True)
        query = query.exclude(owner__in=blocks)
    process = lambda r: serialize(r, ['id', 'name', 'description', 'photo_url'])
    return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=12))

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return JsonResponse(restaurant.get_json(request.user))

def process_cartitem(item):
    return {
        'id': item.id,
        'name': item.menuitem.name,
        'price': item.menuitem.price,
        'menuitem_id': item.menuitem.id,
        'quantity': item.quantity,
    }

@user_role_required
def cart_detail(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    cart = Cart.objects.filter(user=request.user).prefetch_related('cartitem_set__menuitem').first()
    if not cart:
        return JsonResponse({})
    return JsonResponse({
        'restaurant_id': cart.restaurant_id,
        'items': [process_cartitem(item) for item in cart.cartitem_set.all()],
    })


@user_role_required
def cart_add(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    menuitem = get_object_or_404(MenuItem, id=data.get('item_id'))
    restaurant = menuitem.menusection.restaurant
    cart, _new = Cart.objects.get_or_create(user=request.user, defaults={'restaurant': restaurant})
    if not cart.restaurant == restaurant:
        cart.cartitem_set.all().delete()
        cart.restaurant = restaurant
        cart.save()

    cartitem, _new = CartItem.objects.get_or_create(cart=cart, menuitem=menuitem)
    cartitem.quantity += 1
    cartitem.save()
    return cart_detail(request)


@user_role_required
def cart_remove(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    cartitem = get_object_or_404(CartItem, cart__user=request.user, menuitem_id=data.get('item_id'))
    cartitem.quantity -= 1
    cartitem.save()
    if cartitem.quantity < 1:
        cartitem.delete()
    return cart_detail(request)


@user_role_required
def cart_checkout(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(
        restaurant=cart.restaurant,
        user=cart.user,
    )
    order.set_status('placed')
    for cartitem in cart.cartitem_set.all():
        order.total_price += cartitem.quantity * cartitem.menuitem.price
        order.total_items += cartitem.quantity
        orderitem = order.orderitem_set.create(
            menuitem=cartitem.menuitem,
            quantity=cartitem.quantity
        )
    order.save()
    cart.delete()
    return JsonResponse({ "order_id": order.id })


def order_detail(request, order_id):
    q = Order.objects.filter(id=order_id)
    q = q.select_related('restaurant__owner', 'user')
    q = q.prefetch_related('orderstatusupdate_set')
    order = q.first()
    if not (order and order.user_can_see_order(request.user)):
        return JsonResponse({}, status=404)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8') or "{}")
        order = get_object_or_404(Order, id=order_id)
        if data.get('status'):
            if not order.user_can_set_status(request.user, data['status']):
                message = f'You cannot set status {data["status"]}'
                return JsonResponse({ 'message': message }, status=403)
            order.set_status(data.get('status'))
        if data.get('action'):
            owner = order.restaurant.owner
            if request.user != owner:
                message = "Only the owner can block users"
                return JsonResponse({ 'message': message }, status=403)
            if data['action'] == 'block':
                OwnerBlock.objects.get_or_create(user=order.user, owner=owner)
            if data['action'] == 'unblock':
                OwnerBlock.objects.filter(user=order.user, owner=owner).delete()

    return JsonResponse(serialize_order(order, request.user))

def serialize_order(order, user):
    attrs = [
        'user_id',
        'user_name',
        'user_avatar_url',
        'restaurant_photo_url',
        'id',
        'status',
        'status_history',
        'restaurant_name',
        'items',
        'created',
        'total_items',
        'total_price',
    ]
    data = serialize(order, attrs)
    data['allowed_status'] = order.get_allowed_status(user)
    data['is_blocked'] = OwnerBlock.objects.filter(owner=order.restaurant.owner, user=order.user).exists()
    data['is_owner'] = order.restaurant.owner == user
    return data

def order_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({ 'items': [] })

    if request.user.role == 'user':
        query = request.user.order_set.all()
    elif request.user.role == 'owner':
        query = Order.objects.filter(restaurant__owner=request.user)

    if request.GET.get('user_id'):
        query = query.filter(user_id=request.GET['user_id'])
    if request.GET.get('restaurant_id'):
        query = query.filter(restaurant_id=request.GET['restaurant_id'])
    query = query.select_related('restaurant', 'user').prefetch_related('orderstatusupdate_set')
    process = lambda o: serialize_order(o, request.user)
    return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=3))
