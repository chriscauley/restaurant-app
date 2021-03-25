from django.http import JsonResponse
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

def handler404(request, exception='404: Not Found'):
    return JsonResponse({'message': str(exception)}, status=404)