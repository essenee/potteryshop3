import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse, urljoin

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
            line_items = data.get('line_items', [])
            cancel_url = data.get('cancel_url')

            if not line_items:
                return JsonResponse({'error': 'No items in cart'}, status=400)

            # Validate each item
            for item in line_items:
                if not all([item.get('price'), item.get('title'), item.get('quantity')]):
                    missing = [k for k, v in {'price': item.get('price'), 'title': item.get('title'), 'quantity': item.get('quantity')}.items() if not v]
                    return JsonResponse({'error': f'Missing required fields in item: {missing}'}, status=400)

            # Convert prices to cents and validate URLs
            stripe_line_items = []
            domain_url = request.build_absolute_uri('/')[:-1]
            for item in line_items:
                try:
                    price_in_cents = int(float(item['price']) * 100)
                except (ValueError, TypeError) as e:
                    return JsonResponse({'error': f'Invalid price format: {item["price"]}'}, status=400)

                # Validate image_url
                image_url = item.get('image_url', '')
                if image_url:
                    parsed_url = urlparse(image_url)
                    if not (parsed_url.scheme in ['http', 'https'] and parsed_url.netloc and parsed_url.path.startswith('/media/')):
                        print(f"Invalid image_url, omitting: {image_url}")
                        image_url = ''
                    else:
                        # Ensure absolute URL
                        image_url = urljoin(domain_url, image_url)
                        print(f"Normalized image_url: {image_url}")

                stripe_line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': price_in_cents,
                        'product_data': {
                            'name': item['title'],
                            'images': [image_url] if image_url else [],
                        },
                    },
                    'quantity': item['quantity'],
                })

            # Validate cancel_url
            default_cancel_url = urljoin(domain_url, '/payments/cancel/')
            if cancel_url:
                parsed_cancel_url = urlparse(cancel_url)
                if not (parsed_cancel_url.scheme in ['http', 'https'] and parsed_cancel_url.netloc):
                    print(f"Invalid cancel_url, using default: {cancel_url}")
                    cancel_url = default_cancel_url
                else:
                    cancel_url = urljoin(domain_url, parsed_cancel_url.path)
            else:
                cancel_url = default_cancel_url

            # Validate success_url
            success_url = urljoin(domain_url, '/payments/success/')
            print(f"Stripe line items: {stripe_line_items}, Success URL: {success_url}, Cancel URL: {cancel_url}")

            checkout_session = stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=cancel_url,
                payment_method_types=['card'],
                mode='payment',
                line_items=stripe_line_items,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Server error: {str(e)}")
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class SuccessView(TemplateView):
    template_name = 'payments/success.html'

class CancelView(TemplateView):
    template_name = 'payments/cancel.html'

@csrf_exempt
def add_to_cart(request):
    """Add a product to the session-based cart."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            title = data.get('title')
            price = data.get('price')
            image_url = data.get('image_url')

            if not all([product_id, title, price]):
                missing = [k for k, v in {'product_id': product_id, 'title': title, 'price': price}.items() if not v]
                return JsonResponse({'error': f'Missing required fields: {missing}'}, status=400)

            # Initialize cart in session
            cart = request.session.get('cart', {})
            # Add or update item (increment quantity if exists)
            cart_item = cart.get(product_id, {'title': title, 'price': price, 'image_url': image_url, 'quantity': 0})
            cart_item['quantity'] += 1
            cart[product_id] = cart_item
            request.session['cart'] = cart
            request.session.modified = True

            print(f"Cart updated: {cart}")
            return JsonResponse({'success': True, 'message': 'Product added to cart'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def cart_view(request):
    """Display the cart page."""
    cart = request.session.get('cart', {})
    cart_items = [
        {
            'product_id': product_id,
            'title': item['title'],
            'price': float(item['price']),
            'image_url': item['image_url'],
            'quantity': item['quantity'],
            'total': float(item['price']) * item['quantity']
        }
        for product_id, item in cart.items()
    ]
    total_price = sum(item['total'] for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'domain_url': request.build_absolute_uri('/')[:-1]
    }
    return render(request, 'payments/cart.html', context)

@csrf_exempt
def update_cart(request):
    """Update quantities in the cart."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 0)

            if not product_id or quantity < 0:
                return JsonResponse({'error': 'Invalid product_id or quantity'}, status=400)

            cart = request.session.get('cart', {})
            if product_id in cart:
                if quantity == 0:
                    del cart[product_id]
                else:
                    cart[product_id]['quantity'] = quantity
                request.session['cart'] = cart
                request.session.modified = True
                print(f"Cart updated: {cart}")
                return JsonResponse({'success': True, 'message': 'Cart updated'})
            return JsonResponse({'error': 'Product not in cart'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def clear_cart(request):
    """Clear the cart after checkout."""
    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True
        print("Cart cleared")
        return JsonResponse({'success': True, 'message': 'Cart cleared'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)