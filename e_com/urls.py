
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
    
    path('auth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


