from datetime import date
from django.core.checks.messages import Error
from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LC
from .models import FG
from .serializers import CreateLCSerializer, EditLCSerializer, LCSerializer
import dateutil # 이거 왜 경고 뜨는지 아시는분?

# Create your views here.
class LCAPI(APIView):
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
        data["schedule"] = dateutil.parser.parse(date["schedule"])
        serializer = CreateLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})
        
        try:
            # 로그인 fg id 어떻게 가져오나요?
            fg = FG.objects.get(name=data["fg"])
        except FG.DoesNotExist:
            return Response({"error": True, "data": "FG does not exist"})

        LC.objects.create(fg=fg,
                          name=data["name"],
                          #total=data["total"],
                          schedule=data["schedule"])
        return Response({"error": False, "data":serializer.data})

    def put(self, request):
        data = request.data
        data["schedule"] = dateutil.parser.parse(date["schedule"])
        serializer = EditLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})

        try:
            lc = LC.objects.get(name=data["name"])
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        for k, v in data.items():
            setattr(lc, k, v)
        lc.save()

        return Response({"error":False, "data":None})

@api_view(['GET'])
def getLC(request):
    # 로그인한 fg id를 어떻게 가져오죠?
    fg_id = request.GET.get("fg")
    if not fg_id:
        return Response({"error":True, "data": "FG does not exist"})
    
    try:
        queryset = LC.objects.get(fg=fg_id)
        # schedule 대로 정렬 어떻게 해요?
        data = LCSerializer(queryset, many=True).data
    except LC.DoesNotExist:
        return Response({"error": True, "data": "LC does not exist"})
    
    return Response({"error": False, "data":data})