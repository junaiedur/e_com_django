from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_from_cart, name='remove_cart'),
    path('delete_cart/<int:product_id>/<int:cart_item_id>/', views.remove, name='delete_cart'),
    # path('cart_item_increment/<int:product_id>/<int:cart_item_id>/', views.cart_item_increment, name='cart_item_increment'),
    #path('cart_item_decrement/<int:product_id>/<int:cart_item_id> 
    #checkout page desing:
    path('checkout/',views.checkout, name='checkout'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
     path('select_delivery/', views.select_delivery_method, name='select_delivery'),
    # path('cart/', views.cart, name='cart'),
]