from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('store/', include("store.urls")),
    path('cart/', include("carts.urls")),
    path('account/', include("accounts.urls")),
    path('coupon/', include("Coupon.urls")),
    path('payments/', include("payment.urls")),
    path('order/', include("order.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('reviews/', include('reviews.urls')),
<<<<<<< HEAD
    
    path('auth/', include('social_django.urls', namespace='social')),
=======
    path('oauth/', include('social_django.urls', namespace='social')),
>>>>>>> c0daccab1cc38d897fc9d768899d3c06278397b8
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


