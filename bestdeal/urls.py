from django.urls import path
from bestdeal.views import best_deals

urlpatterns = [
    path('best-deals/', best_deals, name='best_deals'),
]
