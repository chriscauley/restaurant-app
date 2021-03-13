from django.http import JsonResponse
from django.contrib.auth import logout

user_attrs = ['id', 'email', 'username', 'role']

def whoami(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    return JsonResponse({'user': { a: getattr(request.user,a) for a in user_attrs}})

def logout_ajax(request):
    logout(request)
    return JsonResponse({})