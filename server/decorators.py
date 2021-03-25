from django.http import JsonResponse

def user_role_required(view_function):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': '401: Unauthorized'}, status=401)
        if not request.user.role == 'user':
            return JsonResponse({'message': '403: Forbidden'}, status=403)
        return view_function(request, *args, **kwargs)
    return wrapped
