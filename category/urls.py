# your_app/urls.py
from django.urls import path
from . import views
from store import views
urlpatterns = [
 # Most specific
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:subsubcategory_slug>/<slug:product_slug>/', views.product_detail, name='product_detail_subsub'),
    # Less specific
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.product_detail, name='product_detail_sub'),
    # Even less specific
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail_category'),
    # Generic fallback
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail_generic'),
]