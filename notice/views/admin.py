from ..models import Comment, Notice
from ..serializers import CommentAdminSerializer, CreateNoticeSerializer, EditNoticeSerializer, NoticeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from fnet_api.csrf import CSRFExemptAPIView

class NoticeAdminAPI(CSRFExemptAPIView):
    def post(self, request):
        """
        create notice
        """
        serializer = CreateNoticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        notice = Notice.objects.create(title=data["title"],
                                       content=data["content"],
                                       created_by=request.user)
        return Response({"error": False, "data": NoticeSerializer(notice).data})

    def get(self, request):
        """
        get a notice or all notice list
        """
        error = False
        notice_id = request.GET.get("id")
        if notice_id:
            try:
                notice = Notice.objects.get(id=notice_id)
                data = NoticeSerializer(notice).data
                return Response({"error": error, "data": data})
            except Notice.DoesNotExist:
                msg = "Notice does not exist"
                error = True
                return Response({"error": error, "data": msg})

        notices = Notice.objects.all().order_by("-create_time")
        count = notices.count()
        results = NoticeSerializer(notices, many=True).data
        data = {"results": results, "total": count}
        return Response({"error": error, "data": data})

    def put(self, request):
        """
        edit notice
        """
        serializer = EditNoticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        error = False
        try:
            notice = Notice.objects.get(id=data.pop("id"))
        except Notice.DoesNotExist:
            msg = "Notice does not exist"
            error = True
            return Response({"error": error, "data": msg})

        notice.title = data["title"]
        notice.content = data["content"]
        notice.save()
        return Response({"error": error, "data": NoticeSerializer(notice).data})

    def delete(self, request):
        """
        delete notice
        """
        error = False
        notice_id = request.GET.get("id")
        if not notice_id:
            msg = "Invalid parameter, id is required"
            error = True
            return Response({"error": error, "data": msg})

        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            msg = "Notice does not exist"
            error = True
            return Response({"error": error, "data": msg})

        notice.delete()
        return Response({"error": error, "data": None})


class CommentAdminAPI(CSRFExemptAPIView):
    def put(self, request):
        """
        check a comment of notice
        """
        serializer = CommentAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        error = False
        notice_id = data["notice_id"]
        comment_id = data["comment_id"]
        try:
            comment = Comment.objects.get(id=comment_id, notice_id=notice_id)
        except Comment.DoesNotExist:
            msg = "Comment does not exist"
            error = True
            return Response({"error": error, "data": msg})

        comment.check = data["check"]
        comment.save()
        return Response({"error": error, "data": None})
