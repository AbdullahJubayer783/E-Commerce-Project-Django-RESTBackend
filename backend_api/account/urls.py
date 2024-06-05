from django.urls import path , include
from backend_api.account.views import UserRegistrationView , UserLoginView,UserProfileView,UserChangePasswordView , SendPasswordResetEmailView , UserPasswordResetView , LogoutAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.views.generic import TemplateView
urlpatterns = [
    
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(),name='logout'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('userchangepassword/', UserChangePasswordView.as_view(),name='userchangepassword'),
    path('userchangepassword/', UserChangePasswordView.as_view(),name='userchangepassword'),
    path('send-user-reset-password/', SendPasswordResetEmailView.as_view(),name='res-pass-send-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(),name='res-pass'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
