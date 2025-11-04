from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # bKash URLs
    path('bkash/initiate/<int:order_id>/', views.initiate_bkash_payment, name='initiate_bkash'),
    path('bkash/callback/', views.bkash_callback, name='bkash_callback'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]