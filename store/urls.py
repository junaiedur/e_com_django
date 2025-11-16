
from django.urls import path
from .import views
from bestdeal.views import best_deals
urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('search/<slug:category_slug>/', views.search, name='search_by_category'),
    path('best-deals/', views.best_deals, name='best_deals'),
]
