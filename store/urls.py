from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('store/category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/subsubcategory/<slug:subsubcategory_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('carts/',include('carts.urls')),
    path('category/',include('category.urls')),
    path('search/', views.search, name='search'),
]

