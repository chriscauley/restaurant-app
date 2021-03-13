from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from server.restaurant.views import restaurant_list

urlpatterns = [
    path('api/restaurant/', restaurant_list),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # pragma: no cover
    from django.views.static import serve
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }),
    ]
