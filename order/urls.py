from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    #payment method Start:
    #path('payment/', views.payment, name='payment'),
    #path('order_complete/', views.order_complete, name='order_complete'),
# order/urls.py তে
    path('payments/', views.payments, name='payments'),    path('order_complete/', views.order_complete, name='order_complete'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<str:order_number>/', views.order_detail, name='order_detail'),
    path('invoice/cart/', views.invoice_cart_pdf, name='invoice_cart_pdf'),
    path('invoice/download/<str:order_number>/', views.download_invoice, name='download_invoice'),  # GET (order complete পেজ থেকে)

]
