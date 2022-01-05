from .models import Notice
from rest_framework import serializers


class CreateNoticeSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()


class EditNoticeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class CommentAdminSerializer(serializers.Serializer):
    notice_id = serializers.IntegerField()
    comment_id = serializers.IntegerField()
    check = serializers.BooleanField()
