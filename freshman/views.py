from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Freshman
from .serializers import FreshmanSerializer

class FreshmanAPI(APIView):
    def get(self, request):
        freshman_id = request.GET.get("id")
        error = False
        if not freshman_id:
            queryset = Freshman.objects.all()
            data = FreshmanSerializer(queryset, many=True).data
        else:
            try:
                queryset = Freshman.objects.get(id=freshman_id)
                data = FreshmanSerializer(queryset).data
            except Freshman.DoesNotExist:
                data = "Freshman does not exist"
                error = True
        return Response({"error": error, "data": data})