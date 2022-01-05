from notice.models import Notice
from ..serializers import NoticeSerializer
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
                data = "Notice does not exist"
                error = True
                return Response({"error": error, "data": data})

        notices = Notice.objects.all().order_by("-create_time")
        count = notices.count()
        results = NoticeSerializer(notices, many=True).data
        data = {"results": results, "total": count}
        return Response({"error": error, "data": data})
