from datetime import date
from django.core.checks.messages import Error
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LC
from .models import FG
from .serializers import CreateLCSerializer, EditLCSerializer, LCSerializer

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
        if not lc_id:
            return Response({"error":True, "data":"Invalid parameter"})

        try:
            queryset = LC.objects.get(id=lc_id)
            queryset.delete()
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        return Response({"error":False, "data":None})
    
    def post(self, request):
        data = request.data
        serializer = CreateLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})
        
        try:
            fg = FG.objects.get(name=data["fg"])
        except FG.DoesNotExist:
            return Response({"error": True, "data": "FG does not exist"})

        LC.objects.create(fg=fg,
                          name=data["name"],
                          total=data["total"],
                          schedule=None)
        return Response({"error": False, "data":serializer.data})

    def put(self, request):
        data = request.data
        serializer = EditLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})

        try:
            lc = LC.objects.get(id=data.pop("id"))
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        for k, v in data.items():
            setattr(lc, k, v)
        lc.save()

        return Response({"error":False, "data":None})