from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    #payment method Start:
    path('payments/', views.payments, name='payments'),
    #payments method end
]