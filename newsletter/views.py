from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_GET
from .models import Subscriber

@require_GET
def unsubscribe(request, email):
    try:
        subscriber = Subscriber.objects.get(email=email)
        subscriber.delete()
        messages.success(request, "You have been successfully unsubscribed.")
    except Subscriber.DoesNotExist:
        messages.error(request, "Email not found in our subscriber list.")
    
    return redirect('home')

@require_POST
@csrf_exempt
def newsletter_signup(request):
    email = request.POST.get('email')
    if email:
        try:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You are already subscribed.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Email is required.'})