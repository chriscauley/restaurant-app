from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from server.restaurant.models import Restaurant, Order, MenuSection, MenuItem, Cart, CartItem, serialize, OwnerBlock
from server.paginate import paginate

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
    # TODO pagination not implemented on front end yet
    return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=60))

def process_cartitem(item):
    return {
        'id': item.id,
        'name': item.menuitem.name,
        'price': item.menuitem.price,
        'menuitem_id': item.menuitem.id,
        'quantity': item.quantity,
    }

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


def cart_remove(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    cartitem = get_object_or_404(CartItem, cart__user=request.user, menuitem_id=data.get('item_id'))
    cartitem.quantity -= 1
    cartitem.save()
    if cartitem.quantity < 1:
        cartitem.delete()
    return cart_detail(request)


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
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8') or "{}")
        order = get_object_or_404(Order, id=order_id)
        if data.get('status'):
            if not order.user_can_set_status(request.user, data['status']):
                raise NotImplementedError(f'TODO {request.user} cannot set status {data["status"]}')
            order.set_status(data.get('status'))
        if data.get('action'):
            owner = order.restaurant.owner
            if request.user != owner:
                raise NotImplementedError('TODO')
            if data['action'] == 'block':
                OwnerBlock.objects.get_or_create(user=order.user, owner=owner)
            if data['action'] == 'unblock':
                OwnerBlock.objects.filter(user=order.user, owner=owner).delete()

    order = get_object_or_404(Order, id=order_id)
    if not order.user_can_see_order(request.user):
        raise NotImplementedError('TODO')
    # TODO this uses so many queries
    attrs = [
        'user_id',
        'user_name',
        'user_avatar_url',
        'id',
        'status',
        'status_history',
        'restaurant_id',
        'restaurant_name',
        'items',
        'created',
        'total_items',
    ]
    data = serialize(order, attrs)
    data['allowed_status'] = order.get_allowed_status(request.user)
    data['is_blocked'] = OwnerBlock.objects.filter(owner=order.restaurant.owner, user=order.user).exists()
    data['is_owner'] = order.restaurant.owner == request.user
    return JsonResponse(data)

def order_list(request):
    if request.user.role == 'user':
        orders = request.user.order_set.all()
    elif request.user.role == 'owner':
        orders = Order.objects.filter(restaurant__owner=request.user)

    if request.GET.get('user_id'):
        orders = orders.filter(user_id=request.GET['user_id'])
    if request.GET.get('restaurant_id'):
        orders = orders.filter(restaurant_id=request.GET['restaurant_id'])
    orders = orders.select_related('restaurant', 'user')
    attrs = [
        'id',
        'restaurant_name',
        'user_name',
        'user_avatar_url',
        'total_items',
        'total_price',
        'created',
        'status',
    ]
    items = []
    for order in orders:
        item = serialize(order, attrs)
        item['allowed_status'] = order.get_allowed_status(request.user)
        items.append(item)
    return JsonResponse({ 'items': items })
