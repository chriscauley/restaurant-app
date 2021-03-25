from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import path

from .utils import form_to_schema
from .urls import urlpatterns
import json

from django import forms

FORMS = {}


def register(form, form_name=None):
    if isinstance(form, str):
        # register is being used as a decorator and args are curried and reversed
        return lambda actual_form: register(actual_form, form_name=form)
    form_name = form_name or form.__name__
    old_form = FORMS.get(form_name, form)
    if repr(form) != repr(old_form):
        e = f"Form with name {form_name} has already been registered.\nOld: {old_form}\nNew:{form}"
        raise ValueError(e)

    FORMS[form_name] = form
    kwargs = dict(form_name=form_name)
    root = f'api/{form_name}/'
    urlpatterns.append(path(root, schema_form, kwargs=kwargs))
    urlpatterns.append(path(root + '<object_id>/', schema_form, kwargs=kwargs))
    return form


def schema_form(request, form_name, object_id=None):
    if not form_name in FORMS:
        raise Http404(f"Form with name {form_name} does not exist")

    form_class = FORMS[form_name]
    _meta  = getattr(form_class, 'Meta', object())
    instance = None

    def check_permission(permission):
        f = getattr(form_class, 'user_can_' + permission, None)
        if f == 'SELF':
            return request.user == instance
        if f == 'ANY':
            return True
        return f and f(instance, request.user)

    if object_id:
        if object_id == "self":
            instance = request.user
        else:
            instance = get_object_or_404(_meta.model, id=object_id)

    kwargs = {}
    if instance:
        kwargs['instance'] = instance
    elif request.method == "GET" and 'schema' in request.GET:
        # schema forms are publicly available if no instance is requested
        schema = form_to_schema(form_class())
        return JsonResponse({'schema': schema})

    if not check_permission('GET'):
        return JsonResponse({'error': 'You do not have access to this resource'}, status=403)

    if request.method == "GET":
        if 'schema' in request.GET:
            schema = form_to_schema(form_class(**kwargs))
            return JsonResponse({'schema': schema})
        if hasattr(instance, 'get_json'):
            return JsonResponse(instance.get_json(request.user))
        raise NotImplementedError('Need to serialize form.')

    if request.method == "POST" or request.method == "PUT":
        if not check_permission('POST'):
            return JsonResponse({'error': 'You cannot edit this resource.'}, status=403)

        data = json.loads(request.body.decode('utf-8') or "{}")
        form = form_class(data, **kwargs)

        form.request = request
        if form.is_valid():
            instance = form.save()
            data = {}
            if instance and hasattr(instance, 'get_json'):
                data = instance.get_json(request.user)
            return JsonResponse(data)
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)

    if request.method == "DELETE":
        if instance and hasattr(form_class, 'user_can_DELETE') and check_permission('DELETE'):
            instance.delete()
            return JsonResponse({})
        return JsonResponse({'error': 'You cannot edit this resource.'}, status=403)

    return JsonResponse({}, status=405)