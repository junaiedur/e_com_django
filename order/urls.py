from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    #payment method Start:
    #path('payment/', views.payment, name='payment'),
    #path('order_complete/', views.order_complete, name='order_complete'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
]