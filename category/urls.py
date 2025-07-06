# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... existing paths ...
    path('', views.products_by_category, {'category_slug': None, 'subcategory_slug': None, 'subsubcategory_slug': None}, name='store'), # Example for a main store view
    path('<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.products_by_subcategory, name='products_by_subcategory'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:subsubcategory_slug>/', views.products_by_subsubcategory, name='products_by_subsubcategory'),
]