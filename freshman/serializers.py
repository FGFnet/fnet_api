
from django.db.models.fields import CharField
from rest_framework import serializers
from .models import Freshman


class FreshmanSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Freshman
        fields = '__all__'

    def get_phone_number(self, obj):
        return obj.phone_number[4:8]

class CreateFreshmanSerializer(serializers.Serializer):
    lc = serializers.CharField()
    name = serializers.CharField(max_length=30)
    # TODO: Add validation(xxx-xxxx-xxx)
    phone_number = serializers.CharField(max_length=13)
    register = serializers.BooleanField()
    department = serializers.ChoiceField(["인문사회계열", "사회과학계열", "공학계열", "자연과학계열"], allow_blank=True)

class FreshmanFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class EditFreshmanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    lc = serializers.CharField()
    name = serializers.CharField(max_length=30)
    # TODO: Add validation(xxx-xxxx-xxx)
    phone_number = serializers.CharField(max_length=13)
    register = serializers.BooleanField()
    department = serializers.ChoiceField(["인문사회계열", "사회과학계열", "공학계열", "자연과학계열"], allow_blank=True)

class registerFreshmanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    register = serializers.BooleanField()