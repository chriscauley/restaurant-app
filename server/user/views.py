from django.http import JsonResponse

user_attrs = ['id', 'email', 'username', 'role']

def whoami(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    return JsonResponse({a: getattr(request.user,a) for a in user_attrs})