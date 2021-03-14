from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from server.restaurant.models import Restaurant, Order, MenuItem
from server.paginate import paginate

restaurant_attrs = ['id', 'name', 'description', 'owner_ids', 'photo_url']

def restaurant_list(request):
    query = Restaurant.objects.all()
    process = lambda r: {attr: getattr(r, attr) for attr in restaurant_attrs}
    # TODO pagination not implemented on front end yet
    return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=60))