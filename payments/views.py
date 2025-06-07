import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

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
    if request.method == 'POST':
        try:
            print("Request body:", request.body.decode('utf-8'))
            data = json.loads(request.body)
            price = data.get('price')
            title = data.get('title')
            image_url = data.get('image_url')
            cancel_url = data.get('cancel_url')

            print(f"Received: price={price}, title={title}, image_url={image_url}, cancel_url={cancel_url}")

            if not all([price, title]):
                missing = [k for k, v in {'price': price, 'title': title}.items() if not v]
                return JsonResponse({'error': f'Missing required fields: {missing}'}, status=400)

            try:
                price_in_cents = int(float(price) * 100)
            except (ValueError, TypeError) as e:
                return JsonResponse({'error': f'Invalid price format: {price}'}, status=400)

            # Use the request's scheme and host for the domain
            domain_url = request.build_absolute_uri('/')[:-1]  # e.g., https://abc123.ngrok.io
            absolute_image_url = request.build_absolute_uri(image_url) if image_url else ''
            default_cancel_url = domain_url + '/payments/cancel/'
            final_cancel_url = cancel_url or default_cancel_url

            print(f"Absolute image URL: {absolute_image_url}, Final cancel URL: {final_cancel_url}")

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/payments/success/',
                cancel_url=final_cancel_url,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': price_in_cents,
                            'product_data': {
                                'name': title,
                                'images': [absolute_image_url] if absolute_image_url else [],
                            },
                        },
                        'quantity': 1,
                    },
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

class CancelView(TemplateView):
    template_name = 'payments/cancel.html'