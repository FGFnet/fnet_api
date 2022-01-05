from ..models import Comment, Notice
from ..serializers import CommentSerializer, CreateCommentSerializer, EditCommentSerializer, NoticeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class NoticeAPI(APIView):
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


class NoticeCommentAPI(APIView):
    def post(self, request):
        """
        create comment of a notice
        """
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        error = False
        try:
            notice = Notice.objects.get(id=data.pop("notice_id"))
        except Notice.DoesNotExist:
            msg = "Notice does not exist"
            error = True
            return Response({"error": error, "data": msg})

        comment = Comment.objects.create(content=data["content"],
                                         created_by=request.user,
                                         notice=notice)
        return Response({"error": error, "data": CommentSerializer(comment).data})

    def get(self, request):
        """
        get comment list of a notice
        """
        error = False
        notice_id = request.GET.get("notice_id")
        if not notice_id:
            msg = "Invalid parameter, notice_id is required"
            error = True
            return Response({"error": error, "data": msg})

        comments = Comment.objects.filter(notice_id=notice_id).order_by("create_time")
        count = comments.count()
        results = CommentSerializer(comments, many=True).data
        data = {"results": results, "total": count}
        return Response({"error": error, "data": data})

    def put(self, request):
        """
        edit comment
        """
        serializer = EditCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        error = False
        try:
            comment = Comment.objects.get(id=data.pop("id"))
        except Comment.DoesNotExist:
            msg = "Comment does not exist"
            error = True
            return Response({"error": error, "data": msg})

        if not comment.created_by == request.user:
            msg = "It is not user's comment"
            error = True
            return Response({"error": error, "data": msg})

        comment.content = data["content"]
        comment.save()
        return Response({"error": error, "data": CommentSerializer(comment).data})

    def delete(self, request):
        """
        delete comment
        """
        error = False
        comment_id = request.GET.get("id")
        if not comment_id:
            msg = "Invalid parameter, id is required"
            error = True
            return Response({"error": error, "data": msg})

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            msg = "Comment does not exist"
            error = True
            return Response({"error": error, "data": msg})

        comment.delete()
        return Response({"error": error, "data": None})
