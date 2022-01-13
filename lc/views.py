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
    # LC id가 있으면 해당 LC 정보, 없으면 전체 LC return
    def get(self, request):
        # user = request.user
        # if user.is_authenticated:
        #     return  Response({"error": True, "data": "login required"})
        print(request)
        # lc_id = request.GET.get("id")
        error = False
        lc_id = False
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
    
    # 해당 LC id의 LC 정보 삭제
    def delete(self, request):
        if request.user.is_authenticated:
            return  Response({"error": True, "data": "login required"})
        lc_id = request.GET.get("id")
        if not lc_id:
            return Response({"error":True, "data":"Invalid parameter"})

        try:
            queryset = LC.objects.get(id=lc_id)
            queryset.delete()
        except LC.DoesNotExist:
            return Response({"error":True, "data":"LC does not exist"})
        
        return Response({"error":False, "data":None})
    
    # LC 정보 등록
    def post(self, request):
        #user = request.user
        # if user.is_authenticated:
        #     return  Response({"error": True, "data": "login required"})
        data = request.data
        data['schedule'] = dateutil.parser.parse(data["schedule"]).now().date()

        serializer = CreateLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})
        
        # is authenticated로 확인된건가?, fg id랑 user id랑 똑같은건가?
        # try:
        #     fg = FG.objects.get(id=user.id)
        # except FG.DoesNotExist:
        #     return Response({"error": True, "data": "FG does not exist"})

        # fg_n인지 fg_s인지 어떻게 구분?
        # if user.department == 'n':
        #     LC.objects.create(fg_n=fg,
        #                     fg_s=null,
        #                     name=data["name"],
        #                     schedule=data["schedule"])
        # else:
        #     LC.objects.create(fg_n=null,
        #                     fg_s=fg,
        #                     name=data["name"],
        #                     schedule=data["schedule"])
        
        LC.objects.create(fg_n=None,
                            fg_s=None,
                            name=data["name"],
                            schedule=data["schedule"])
        return Response({"error": False, "data":serializer.data})

    # LC id로 LC 정보 수정
    def put(self, request):
        user = request.user
        if user.is_authenticated:
            return  Response({"error": True, "data": "login required"})
        
        data = request.data
        data["schedule"] = dateutil.parser.parse(date["schedule"]).date()
        serializer = EditLCSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": True, "data":"Not valid"})

        try:
            lc = LC.objects.get(id=data.pop("id"))
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

# LC 이름으로 LC정보 return
@api_view(['GET'])
def getLC(self, request):
        # user = request.user
        # if user.is_authenticated:
        #     return  Response({"error": True, "data": "login required"})
        # lc_id = request.GET.get("id")
        # error = False
        # print(request)
        # lc_name = request.GET.get("name")
        # if not lc_name:
        #     quieryset = LC.objects.all()
        #     data = LCSerializer(quieryset, many=True).data
        # else:
        #     try:
        #         queryset = LC.objects.get(name=lc_name)
        #         data = LCSerializer(queryset).data
        #     except LC.DoesNotExist:
        #         data = "LC does not exist"
        #         error = True
        return Response({"error":true, "data":true})

@api_view(['GET'])
# FG의 담당 모든 LC 목록을 return
def getLCList(self, request):
    user = request.user
    # if user.is_authenticated:
    #         return  Response({"error": True, "data": "Login required"})
    
    # try:
    #     if user.department == 'n':
    #         queryset = LC.objects.get(fg_n=user.id)
    #     else:
    #         queryset = LC.objects.get(fg_s=user.id)
    #     data = LCSerializer(queryset, many=True).data
    # except LC.DoesNotExist:
    #     return Response({"error": True, "data": "LC does not exist"})
    
    queryset = LC.objects.all()
    data = LCSerializer(queryset, many=True)
    return Response({"error": False, "data":data})