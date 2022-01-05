from django.db.models.fields import Field
from rest_framework import serializers
from .models import LC

class LCSerializer(serializers.ModelSerializer):
    class Meta:
        model = LC
        Fields = '__all__'

class CreateLCSerializer(serializers.Serializer):
    fg_id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)
    total = serializers.IntegerField()