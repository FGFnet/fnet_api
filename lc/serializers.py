from django.db.models.fields import Field
from rest_framework import serializers
from .models import LC

class LCSerializer(serializers.ModelSerializer):
    class Meta:
        model = LC
        fields = '__all__'

class CreateLCSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    schedule = serializers.DateField()

class EditLCSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    schedule = serializers.DateField()
