from rest_framework import serializers
from django.contrib.auth.models import User

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email']
        read_only_fields=['username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email']

class OtpSerializer(serializers.Serializer):
    opt=serializers.CharField()

class PasswordSerializer(serializers.Serializer):
    password=serializers.CharField()
