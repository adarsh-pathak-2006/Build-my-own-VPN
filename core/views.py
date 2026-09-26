from .models import Summary
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import TranscriptFetch
from .serializer import SummaryGenerationSerializer, SummaryGenerationListSerializer
from rest_framework.generics import RetrieveAPIView
from config.pagination import GeneralPagination

class GeneratedSummaryListAPI(APIView):
    def get(self, request):
        paginator=GeneralPagination()
        data=paginator.paginate_queryset(Summary.objects.select_related('user').filter(user=self.request.user).order_by("-time"))
        serial=SummaryGenerationListSerializer(data, many=True)
        return paginator.get_paginated_response(serial.data)

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
        return Response(serial.errors, status=400)