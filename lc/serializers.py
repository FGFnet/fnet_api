from django.db.models.fields import Field
from rest_framework import serializers
from .models import LC

class LCSerializer(serializers.ModelSerializer):
    class Meta:
        model = LC
        Fields = '__all__'

class CreateLCSerializer(serializers.Serializer):
    fg = serializers.CharField()
    name = serializers.CharField(max_length=32)
    total = serializers.IntegerField()
    schedule = serializers.DateField()

class EditLCSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fg = serializers.CharField()
    name = serializers.CharField(max_length=32)
    schedule = serializers.DateField()