from rest_framework.serializers import ModelSerializer
from .models import Summary
from authentication.serializer import UserGetSerializer

class SummaryGenerationListSerializer(ModelSerializer):
    class Meta:
        model=Summary
        fields=['user', 'link', 'time']
        read_only_fields=['user', 'link', 'time']

class SummaryGenerationSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Summary
        fields='__all__'
        read_only_fields=['transcript', 'summary', 'time']