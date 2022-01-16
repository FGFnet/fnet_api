from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view

from lc.models import LC
from .models import Freshman
from .serializers import (CreateFreshmanSerializer, EditFreshmanSerializer, FreshmanSerializer, 
                            FreshmanFileUploadSerializer, registerFreshmanSerializer, FreshmanTableDataSerializer)

from django.db import transaction, IntegrityError
from openpyxl import load_workbook
from fnet_api.csrf import CSRFExemptAPIView

class FreshmanAPI(APIView):
    def get(self, request):
        freshman_id = request.GET.get("id")
        error = False
        if freshman_id:
            try:
                queryset = Freshman.objects.get(id=freshman_id)
                data = FreshmanSerializer(queryset).data
            except Freshman.DoesNotExist:
                data = "Freshman does not exist"
                error = True
        else:
            queryset = Freshman.objects.all()
            data = FreshmanSerializer(queryset, many=True).data

        return Response({"error": error, "data": data})
    
    def post(self, request):
        data = request.data
        serializer = CreateFreshmanSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        lc_name = data['lc']
        try:
            lc = LC.objects.get(name=lc_name)
        except LC.DoesNotExist:
            return Response({"error": True, "data": "LC does not exist"})

        Freshman.objects.create(lc=lc,
                                name=data["name"],
                                phone_number=data["phone_number"],
                                register=data["register"],
                                department=data["department"])

        return Response({"error": None, "data": serializer.data})
    
    def put(self, request):
        data = request.data
        serializer = EditFreshmanSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        lc_name = data.pop("lc")
        try:
            lc = LC.objects.get(name=lc_name)
            data["lc"] = lc
        except LC.DoesNotExist:
            return Response({"error": True, "data": "LC does not exist"})
        
        try:
            freshman = Freshman.objects.get(id=data.pop("id"))
        except Freshman.DoesNotExist:
            return Response({"error": True, "data": "Freshman does not exist"})

        for k, v in data.items():
            setattr(freshman, k, v)
        freshman.save()
        return Response({"error": False, "data": FreshmanSerializer(freshman).data})

    def delete(self, request):
        freshman_id = request.GET.get("id")
        if freshman_id:
            Freshman.objects.filter(id=freshman_id).delete()
        return Response({})
    

class FreshmanFileUploadAPI(CSRFExemptAPIView):
    parser_classes = (MultiPartParser,)

    # TODO: Add exception handling
    def post(self, request):
        serializer = FreshmanFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        rows = load_workbook(file).active.rows
        data_list = [[cell.value for cell in row] for row in rows]
        # remove header
        data_list.pop(0)

        freshman_list = []
        for data in data_list:
            # lc_name = data[5]
            lc_name = "LC10"
            try:
                lc = LC.objects.get(name=lc_name)
            except LC.DoesNotExist:
                continue
            if Freshman.objects.filter(name=data[0], phone_number=data[3]).exists():
                continue
            freshman_list.append(Freshman(lc=lc, name=data[0], department=data[1], phone_number=data[3]))
        try:
            with transaction.atomic():
                Freshman.objects.bulk_create(freshman_list)
        except IntegrityError as e:
            return Response({"data": str(e).split("\n")[0]})
        return Response({})



class RegisterFreshmanAPI(CSRFExemptAPIView):
    def put(self, request):
        data = request.data
        serializer = registerFreshmanSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            freshman = Freshman.objects.get(id=data["id"])
        except Freshman.DoesNotExist:
            return Response({"error": True, "data": "Freshman does not exist"})
        
        freshman.register = not freshman.register
        freshman.save()
        return Response({"error": False, "data": {}})


@api_view(['GET'])
def getLCMemberList(request):
    lc_name = request.GET.get("name")
    register = request.GET.get("register")

    if not lc_name:
        return Response({"error": True, "data": "LC name is required"})

    try:
        lc_id = LC.objects.get(name=lc_name)
    except LC.DoesNotExist:
        return Response({"error": True, "data": "LC does not exist"})

    if not register:
        queryset = Freshman.objects.filter(lc_id=lc_id)
    else:
        queryset = Freshman.objects.filter(lc_id=lc_id, register=True)

    data = FreshmanTableDataSerializer(queryset, many=True).data
    return Response({"error": False, "data": data})



@api_view(['GET'])
def searchFreshman(request):
    query = request.GET.get("query")
    if not query:
        freshman = Freshman.objects.all()
    else:
        freshman = Freshman.objects.filter(name=query)
    return Response({"error": False, "data": FreshmanSerializer(freshman, many=True).data})