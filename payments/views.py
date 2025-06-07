import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_config(request):
    """Return the Stripe public key for client-side use."""
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def create_checkout_session(request):
    """Create a Stripe checkout session."""
    if request.method == 'POST':
        try:
            # Define your domain (update with your production domain)
            domain_url = 'http://localhost:8000'  # Change for production
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/payments/success/',
                cancel_url=domain_url + '/payments/cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 2000,  # Amount in cents (e.g., $20.00)
                            'product_data': {
                                'name': 'Sample Product',
                            },
                        },
                        'quantity': 1,
                    },
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class SuccessView(TemplateView):
    """View for the success page after payment."""
    template_name = 'payments/success.html'

class CancelView(TemplateView):
    """View for the cancel page if payment is canceled."""
    template_name = 'payments/cancel.html'

def payment_page(request):
    """Render the payment form page."""
    return render(request, 'payments/payment_form.html')