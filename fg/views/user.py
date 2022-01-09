from fg.models import FG
from fg.serializers import FGSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class FGAPI(APIView):
    def get(self, request):
        fg_id = request.GET.get("id")
        error = False
        if fg_id:
            try:
                fg = FG.objects.filter(id=fg_id)
                data = FGSerializer(fg).data
            except:
                data = "FG does not exist"
                error = True
        else:
            data = "Invalid parameter, id is required."
            error = True
        return Response({"error": error, "data": data})