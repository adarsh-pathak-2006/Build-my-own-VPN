from django.urls import path
from .views import OtpCreationAPI, OtpVerificationAPI, PasswordSetupAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('otp-creation/', OtpCreationAPI.as_view()),
    path('otp-verify/<str:id>/', OtpVerificationAPI.as_view()),
    path('password-setup/<str:id>/', PasswordSetupAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('apt/token/refresh/', TokenRefreshView.as_view()),
]
