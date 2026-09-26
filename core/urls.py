from django.urls import path
from .views import GeneratedSummaryListAPI, GeneratedSummaryDetailAPI, SummaryCreationAPI

urlpatterns = [
    path('all/', GeneratedSummaryListAPI.as_view()),
    path('all/<int:pk>/', GeneratedSummaryDetailAPI.as_view()),
    path('create/', SummaryCreationAPI.as_view())
]
