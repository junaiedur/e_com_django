from django.urls import path, include
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/',views.dashboard, name ='dashboard'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('forgot-password/',views.forgot_password, name='forgot_password'),
]