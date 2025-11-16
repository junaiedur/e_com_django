from django.urls import path, include
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('home/', views.home, name='home'),
    path('dashboard/',views.dashboard, name ='dashboard'),
    path('', views.dashboard, name='dashboard'),
    
    path('profile/', views.profile, name='profile'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    #path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]