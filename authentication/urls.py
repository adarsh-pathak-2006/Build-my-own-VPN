from django.urls import path
from .views import OtpCreationAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', OtpCreationAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('apt/token/refresh/', TokenRefreshView.as_view()),
]
