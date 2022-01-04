from django.db import models
from rest_framework import serializers
from .models import Freshman


class FreshmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freshman
        Fields = '__all__'