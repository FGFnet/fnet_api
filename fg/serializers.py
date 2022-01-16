from django.db import models
from rest_framework import serializers
from .models import FG
from rest_framework import serializers

from django import forms

class FGSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, default=None)
    class Meta:
        model = FG
        fields = '__all__'

class FGFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class CreateFGSerializer(serializers.Serializer):
    name = serializers.CharField()
    student_id = serializers.CharField()
    is_admin = serializers.BooleanField()
    campus = serializers.CharField()

class FGLoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()

class UserInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_admin = serializers.BooleanField()
    campus = serializers.CharField()