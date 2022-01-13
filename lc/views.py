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
import dateutil.parser
import datetime

# Create your views here.
class LCAPI(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return  Response({"error": True, "data": "login required"})

        error = False
        lc_name = request.GET.get("name")
        if not lc_name:
            quieryset = LC.objects.all()
            data = LCSerializer(quieryset, many=True).data
        else:
            try:
                queryset = LC.objects.get(name=lc_name)
                data = LCSerializer(queryset).data
            except LC.DoesNotExist:
                data = "LC does not exist"
                error = True
        return Response({"error":error, "data":data})
    
    def delete(self, request):
        if request.user.is_authenticated:
            return  Response({"error": True, "data": "login required"})
        
        lc_name = request.GET.get("name")
        if not lc_name:
            return Response({"error":True, "data":"Invalid parameter"})

        try:
            queryset = LC.objects.get(name=lc_name)
            queryset.delete()
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        return Response({"error":False, "data":None})
    
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            return  Response({"error": True, "data": "login required"})
        data = request.data
        data['schedule'] = dateutil.parser.parse(data["schedule"]).date()

        # NO MULTIPLE OBJECT!
        try:
            queryset = LC.objects.get(name=data['name'])
        except LC.DoesNotExist:
            serializer = CreateLCSerializer(data=data)
            if not serializer.is_valid():
                return Response({"error": True, "data":"Not valid"})

            if user.department == 'n':
                LC.objects.create(fg_n=fg,
                                fg_s=null,
                                name=data["name"],
                                schedule=data["schedule"])
            else:
                LC.objects.create(fg_n=null,
                                fg_s=fg,
                                name=data["name"],
                                schedule=data["schedule"])

            return Response({"error": False, "data":serializer.data})

        return Response({"error": True, "data": "LC already exists"})

    def put(self, request):
        user = request.user
        if user.is_authenticated:
            return  Response({"error": True, "data": "login required"})
        
        data = request.data
        data['schedule'] = dateutil.parser.parse(data["schedule"]).date()
        serializer = EditLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})

        try:
            lc = LC.objects.get(name=data['name'])
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        if user.department == 'n':
            lc.fg_n = user.id
        else:
            lc.fg_s = user.id
        
        lc.name = data['name']
        lc.schedule = data['schedule']
        lc.save()

        return Response({"error":False, "data":None})

@api_view(['GET'])
# FG의 담당 모든 LC 목록을 return
def getLCList(self, request):
    user = request.user
    if user.is_authenticated:
            return  Response({"error": True, "data": "Login required"})
    
    try:
        if user.department == 'n':
            queryset = LC.objects.get(fg_n=user.id)
        else:
            queryset = LC.objects.get(fg_s=user.id)
            data = LCSerializer(queryset, many=True).data
    except LC.DoesNotExist:
        return Response({"error": False, "data": None})
    
    return Response({"error": False, "data":data})