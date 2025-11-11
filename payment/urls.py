from django.urls import path
from django.urls import path
from . import views as payment_views           # <— payment app views
from order import views as order_views   
app_name = 'payment'

# urlpatterns = [
    # bKash URLs
#     path('bkash/initiate/<int:order_id>/', views.initiate_bkash_payment, name='initiate_bkash'),
#     path('bkash/callback/', views.bkash_callback, name='bkash_callback'),
#     path('success/', views.payment_success, name='payment_success'),
#     path('failed/', views.payment_failed, name='payment_failed'),
#     path('invoice/<str:order_number>/', views.invoice_view, name='invoice'),
# ]
urlpatterns = [
    # bKash URLs (from payment app)
    path('bkash/initiate/<int:order_id>/', payment_views.initiate_bkash_payment, name='initiate_bkash'),
    path('bkash/callback/', payment_views.bkash_callback, name='bkash_callback'),
    path('success/', payment_views.payment_success, name='payment_success'),
    path('failed/', payment_views.payment_failed, name='payment_failed'),

    # Invoice view (from order app)
    path('invoice/<str:order_number>/', order_views.invoice_view, name='invoice'),
]