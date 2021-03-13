from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from server.restaurant.views import restaurant_list

# need to import these files somewhere to @schema.register the forms
# import server.restaurant.forms
import server.user.forms

urlpatterns = [
    path('api/restaurant/', restaurant_list),
    path('admin/', admin.site.urls),
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
