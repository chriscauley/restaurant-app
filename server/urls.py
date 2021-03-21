from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from server.restaurant.views import restaurant_list, restaurant_detail, cart_detail, cart_add, cart_remove, cart_checkout, order_detail, order_list
from server.user.views import whoami, logout, complete_registration
from server.views import spa

# need to import these files somewhere to @schema.register the forms
import server.restaurant.forms
import server.user.forms

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/restaurant/', restaurant_list),
    path('api/restaurant/<int:restaurant_id>/', restaurant_detail),
    path('api/cart/', cart_detail),
    path('api/cart/add/', cart_add),
    path('api/cart/remove/', cart_remove),
    path('api/cart/checkout/', cart_checkout),
    path('api/order/<int:order_id>/', order_detail),
    path('api/order/', order_list),

    path('api/whoami', whoami),
    path('api/logout', logout),
    path('registration/complete/<str:activation_key>/', complete_registration),

    path('', include('social_django.urls', namespace='social')),
    path('', include('server.schema.urls')),
]

if settings.DEBUG:  # pragma: no cover
    from django.views.static import serve
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }),
    ]

urlpatterns.append(re_path('', spa))
