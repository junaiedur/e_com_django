from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # bKash URLs
    path('initiate-bkash/', views.initiate_bkash_payment, name='initiate_bkash_payment'),
    path('bkash/callback/', views.bkash_payment_callback, name='bkash_payment_callback'),
]