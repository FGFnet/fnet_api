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
from .serializers import LCSerializer, UpdateLCSerialiser
import dateutil.parser
import datetime

# Create your views here.
class LCAPI(APIView):
    def get(self, request):
        user = request.user
        lc_name = request.GET.get("name")
        if lc_name:
            try:
                queryset = LC.objects.get(name=lc_name)
                data = LCSerializer(queryset).data
            except LC.DoesNotExist:
                return Response({"error": True, "data": "LC name error"})
        else:
            if user.campus == 'n':
                queryset = LC.objects.get(fg_n=user.id)
            else:
                queryset = LC.objects.get(fg_s=user.id)
            data = LCSerializer(queryset, many=True).data
        return Response({"error":False, "data":data})
    
    def delete(self, request):
        if request.user.is_authenticated:
            return  Response({"error": True, "data": "login required"})
        
        lc_id = request.GET.get("id")
        if not lc_name:
            return Response({"error":True, "data":"Invalid parameter"})

        try:
            queryset = LC.objects.get(id=lc_id)
            queryset.delete()
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        return Response({"error":False, "data":None})

    def post(self, request):
        data = request.data
        data['schedule'] = dateutil.parser.parse(data["schedule"]).date()

        serializer = updateLCSerializer(data=data)
        if not serializer.is_valid:
            return Response({"error": True, "data":"Not valid"})
        
        data = serializer.data
        old_id = data['old_id']
        if old_id > 0:
            try:
                oldLc = LC.objects.get(id=old_id)
                if user.campus == 'n':
                    oldLc.fg_n = None
                else:
                    oldLc.fg_s = None
            except LC.DoesNotExist:
                return Response({"error":True, "data": "original LC does not exist"})
        
        user = request.user
        try:
            lc = LC.objects.get(name=data['name'])
            if user.campus == 'n':
                lc.fg_n = user.id
            else:
                lc.fg_s = user.id
            
            lc.schedule = data['schedule']
            lc.save()
            
        except LC.DoesNotExist:
            if user.campus == 'n':
                LC.objects.create(fg_n=user.id,
                                fg_s=None,
                                name=data['name'],
                                schedule=data['schedule'])
            else:
                LC.objects.create(fg_n=None,
                                fg_s=user.id,
                                name=data['name'],
                                schedule=data['schedule'])
        
        return Response({"error": False, "data": "success"})
    