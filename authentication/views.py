from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializer import RegisterSerializer, OtpSerializer, PasswordSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model
from .tasks import OTPCreation
import random
from config.cache_keys import otpCacheKey, sessionCacheKey
from django.core.cache import cache
from rest_framework.permissions import AllowAny

User=get_user_model()

class OtpCreationAPI(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'message':'username and email already exists'}, status=400)
            otprefid=str(random.randint(100000, 999999))
            OTPCreation.delay(id=otprefid, email=email)
            cache.set(sessionCacheKey(id=otprefid), {'username':username, 'email':email, 'verified':False}, timeout=500)
            return Response({'message':'OTP generated successfully', "ref_id":otprefid}, status=201)
        return Response(serial.errors, status=400)
    
class OtpVerificationAPI(APIView):
    permission_classes=[AllowAny]
    def post(self, request, id):
        serial=OtpSerializer(data=request.data)
        if serial.is_valid():
            otp=serial.validated_data['otp']
            generated_otp=cache.get(otpCacheKey(id=id))
            if generated_otp:
                if otp==generated_otp:
                    session=cache.get(sessionCacheKey(id=id))
                    if session:
                        session['verified']=True
                        cache.set(sessionCacheKey(id=id), session, timeout=500)
                        return Response({'message':'otp verified successfully you may now set the password'}, status=200)
                    return Response({'message':'registration session expired try registering again'}, status=400)
                return Response({'message':'wrong otp entered enter the correct one'}, status=400)
            return Response({'message':'otp expired try generating new otp'}, status=400)
        return Response(serial.errors, status=400)

class PasswordSetupAPI(APIView):
    permission_classes=[AllowAny]
    def post(self, request, id):
        serial=PasswordSerializer(data=request.data)
        if serial.is_valid():
            password=serial.validated_data['password']
            session_data=cache.get(sessionCacheKey(id=id))
            if not session_data:
                return Response({'message':'registration session expired'}, status=400)
            if not session_data.get('verified'):
                return Response({'message':'OTP not verified...verify otp first'}, status=400)
            User.objects.create_user(username=session_data['username'], email=session_data['email'], password=password)
            cache.delete(otpCacheKey(id=id))
            cache.delete(sessionCacheKey(id=id))
            return Response({'message':'User Registerd Successfully'}, status=201)
        return Response(serial.errors, status=400)