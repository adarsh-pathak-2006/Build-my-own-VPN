from django.shortcuts import render
from .models import Summary
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import TranscriptFetch
from .serializer import SummaryGenerationSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

class GeneratedSummaryListAPI(ListAPIView):
    serializer_class=SummaryGenerationSerializer

    def get_queryset(self):
        return Summary.objects.select_related('user').filter(user=self.request.user)

class GeneratedSummaryDetailAPI(RetrieveAPIView):
    serializer_class=SummaryGenerationSerializer

    def get_queryset(self):
        return Summary.objects.select_related('user').filter(user=self.request.user)

class SummaryCreationAPI(APIView):
    def post(self, request):
        serial=SummaryGenerationSerializer(data=request.data)
        if serial.is_valid():
            data=serial.save()
            TranscriptFetch.delay(id=data.id)
            return Response({'message':'Generation started..might take a moment', 'db_id':data.id})