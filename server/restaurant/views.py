from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from server.restaurant.models import Restaurant, Order, MenuSection, MenuItem, Cart, CartItem
from server.paginate import paginate

restaurant_attrs = ['id', 'name', 'description', 'owner_ids', 'photo_url']
menuitem_attrs = ['id', 'name', 'price', 'description']

def process_restaurant(restaurant):
    return {attr: getattr(restaurant, attr) for attr in restaurant_attrs}

def restaurant_list(request):
    query = Restaurant.objects.all()
    process = process_restaurant
    # TODO pagination not implemented on front end yet
    return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=60))

def process_menusection(menusection):
    return {
        'name': menusection.name,
        'items': [process_menuitem(i) for i in menusection.menuitem_set.all()]
    }

def process_menuitem(menuitem):
    return { attr: getattr(menuitem, attr) for attr in menuitem_attrs }

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    data = process_restaurant(restaurant)
    menusections = restaurant.menusection_set.all().prefetch_related('menuitem_set')
    data['menusections'] = [process_menusection(s) for s in menusections]
    return JsonResponse(data)

def process_cartitem(item):
    return {
        'id': item.id,
        'name': item.menuitem.name,
        'price': item.menuitem.price,
        'menuitem_id': item.menuitem.id,
        'quantity': item.quantity,
    }

def cart_detail(request):
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
        user=cart.user
    )
    for cartitem in cart.cartitem_set.all():
        orderitem = order.orderitem_set.create(
            menuitem=cartitem.menuitem,
            quantity=cartitem.quantity
        )
    cart.delete()
    return JsonResponse({ "order_id": order.id })