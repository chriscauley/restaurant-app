from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from unrest.views import index

from server.restaurant.views import restaurant_detail, restaurant_list, cart_detail, cart_add, cart_remove, cart_checkout, order_detail, order_list
from server.user.views import whoami, logout, complete_registration

# need to import these files somewhere to @schema.register the forms
import server.restaurant.forms
import server.user.forms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/restaurants/', restaurant_list),
    path('api/cart/', cart_detail),
    path('api/cart/add/', cart_add),
    path('api/cart/remove/', cart_remove),
    path('api/cart/checkout/', cart_checkout),
    path('api/order/<int:order_id>/', order_detail),
    path('api/orders/', order_list),
    path('api/restaurant/<int:restaurant_id>/', restaurant_detail),

    path('api/self/', whoami),
    path('api/logout/', logout),
    path('registration/complete/<str:activation_key>/', complete_registration),

    path('', include('social_django.urls', namespace='social')),
    path('', include('unrest.urls')),
    re_path('', index),
]

# TODO abstract 404 into unrest
handler404 = "server.views.handler404"