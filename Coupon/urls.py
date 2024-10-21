# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URLs...
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]
