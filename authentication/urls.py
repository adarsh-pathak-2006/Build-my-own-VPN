from django.urls import path
from .views import RegisterAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('apt/token/refresh/', TokenRefreshView.as_view()),
]
