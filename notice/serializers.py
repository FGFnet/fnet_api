from .models import Comment, Notice
from rest_framework import serializers
from fg.serializers import FGSerializer


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


class CreateCommentSerializer(serializers.Serializer):
    notice_id = serializers.IntegerField()
    content = serializers.CharField()


class EditCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    created_by = FGSerializer()
    class Meta:
        model = Comment
        fields = "__all__"
