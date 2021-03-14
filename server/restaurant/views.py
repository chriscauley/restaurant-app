from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from server.restaurant.models import Restaurant, Order, MenuSection
from server.paginate import paginate

restaurant_attrs = ['id', 'name', 'description', 'owner_ids', 'photo_url']
menuitem_attrs = ['name', 'price', 'description']

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