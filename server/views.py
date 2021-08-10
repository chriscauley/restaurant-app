from django.http import JsonResponse

def handler404(request, exception='404: Not Found'):
    return JsonResponse({'message': str(exception)}, status=404)