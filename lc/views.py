from django.core.checks.messages import Error
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LC
from .serializers import LCSerializer

# Create your views here.
class LcAPI(APIView):
    def get(self, request):
        lc_id = request.GET.get("id")
        error = False
        if not lc_id:
            quieryset = LC.objects.all()
            data = LCSerializer(quieryset, many=True).data
        else:
            try:
                queryset = LC.objects.get(id=lc_id)
                data = LCSerializer(queryset).data
            except LC.DoesNotExist:
                data = "LC does not exist"
                error = True
        return Response({"error":error, "data":data})
    
    def delete(self, request):
        lc_id = request.GET.get("id")
        error, data = False, None
        if not lc_id:
            data = "Invalid parameter"
            error = True
        try:
            queryset = LC.objects.get(id=lc_id)
            queryset.delete()
        except LC.DoesNotExist:
            data = "LC does not exist"
            error = True
        return Response({"error":error, "data":data})
    
    def post(self, request):
        data = request.data
        LC.objects.create(fg_id = data["fg_id"],
                            name = data["name"],
                            total = data["total"],
                            schedule = None)
        return Response({"error": False, "data":None})

    def put(self, request):
        data = request.data
        error = False
        try:
            lc = LC.objects.get(id=data.pop("id"))
        except LC.DoesNotExist:
            error = True
        
        for k, v in data.items():
            setattr(lc, k, v)
        lc.save()

        return Response({"error":error, "data":None})