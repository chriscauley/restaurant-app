from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve

import os

@ensure_csrf_cookie
def spa(request, path='client/dist/index.html'):
    response = serve(
        request,
        os.path.basename(path),
        os.path.dirname(path)
    )
    return response
