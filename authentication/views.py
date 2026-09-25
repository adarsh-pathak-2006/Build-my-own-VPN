from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializer import RegisterSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model
from .tasks import OTPCreation
import random

User=get_user_model()

class OtpCreationAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'message':'username and email already exists'}, status=400)
            otprefid=random.randint(100000, 999999)
            OTPCreation.delay(id=otprefid, email=email)
            return Response({'message':'OTP generated successfully', "ref_id":otprefid}, status=201)
        return Response(serial.errors, status=400)
    
