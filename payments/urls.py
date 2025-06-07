from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.stripe_config, name='stripe_config'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    # path('', views.payment_page, name='payment_page'),  # Root of /payments/
]