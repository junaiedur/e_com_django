from django.urls import path
from . import views
from store import views
urlpatterns = [
    path('', views.store, name='store'),
    path('flash-sale/', views.flash_sale, name='flash_sale'),
]
