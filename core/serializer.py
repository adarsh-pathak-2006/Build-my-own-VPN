from rest_framework.serializers import ModelSerializer
from .models import Summary
from authentication.serializer import UserGetSerializer

class SummaryGenerationSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Summary
        fields=['link']
        read_only_fields=['transcript', 'summary', 'time']