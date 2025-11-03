
from django.urls import path
# payment/urls.py
from django.urls import path
from . import views

# This is optional, but good practice for namespacing
app_name = 'payment'

# The list MUST be named 'urlpatterns' and it must be a list (using [])
urlpatterns = [
    # Add your URL patterns here.
    # If you have none yet, you can leave it empty for now,
    # but it's better to have a placeholder.
    # Example: path('checkout/', views.checkout, name='checkout'),
]