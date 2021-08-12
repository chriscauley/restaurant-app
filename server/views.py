from django.http import JsonResponse
from unrest.user.views import user_json

def handler404(request, exception='404: Not Found'):
    return JsonResponse({'message': str(exception)}, status=404)

user_json.extras = [
    lambda request: {
        'avatar_url': request.user.avatar_url,
        'role': request.user.role,
    }
]