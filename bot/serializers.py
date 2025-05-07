from rest_framework import serializers
from .models import OTPCode


class OTPCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
