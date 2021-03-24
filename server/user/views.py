from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout as _logout, login
from django_registration.backends.activation.views import ActivationView, ActivationError

user_attrs = ['id', 'email', 'username', 'role', 'avatar_url']

def whoami(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    return JsonResponse({'user': { a: getattr(request.user,a) for a in user_attrs}})

def logout(request):
    _logout(request)
    return JsonResponse({})

def complete_registration(request, activation_key):
    view = ActivationView()
    try:
        user = view.activate(activation_key=activation_key)
    except ActivationError:
        return HttpResponseRedirect('/registration/invalid/')
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponseRedirect('/registration/complete/')