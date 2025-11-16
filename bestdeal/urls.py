from django.urls import path
from best.views import best_deals
urlpatterns = [
path('best-deals/', best_deals, name='best_deals'),
]