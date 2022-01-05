from ..models import Notice
from ..serializers import CreateNoticeSerializer, EditNoticeSerializer, NoticeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


def invalid_serializer(self, serializer):
    key, error = self.extract_errors(serializer.errors)
    if key == "non_field_errors":
        msg = error
    else:
        msg = f"{key}: {error}"
    return {"error": True, "data": msg}


class NoticeAdminAPI(APIView):
    def post(self, request):
        """
        create notice
        """
        serializer = CreateNoticeSerializer(data=request.data)
        if not serializer.is_valid():
            error = invalid_serializer(serializer)
            return Response(error)

        error = False
        notice = Notice.objects.create(title=serializer["title"],
                                       content=serializer["content"],
                                       created_by=request.user)
        data = NoticeSerializer(notice).data
        return Response({"error": error, "data": data})

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
                data = "Notice does not exist"
                error = True
                return Response({"error": error, "data": data})

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
        if not serializer.is_valid():
            error = invalid_serializer(serializer)
            return Response(error)

        error = False
        try:
            notice = Notice.objects.get(id=serializer.pop("id"))
        except Notice.DoesNotExist:
            data = "Notice does not exist"
            error = True
            return Response({"error": error, "data": data})

        notice.title = serializer["title"]
        notice.content = serializer["content"]
        notice.save()
        data = NoticeSerializer(notice).data
        return Response({"error": error, "data": data})

    def delete(self, request):
        """
        delete notice
        """
        error = False
        notice_id = request.GET.get("id")
        if not notice_id:
            data = "Invalid parameter, id is required"
            error = True
            return Response({"error": error, "data": data})

        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            data = "Notice does not exist"
            error = True
            return Response({"error": error, "data": data})

        notice.delete()
        return Response({"error": error, "data": None})
