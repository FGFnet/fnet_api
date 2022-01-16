from ..models import FG
from ..serializers import (FGSerializer, FGFileUploadSerializer, CreateFGSerializer)
from freshman.models import Freshman
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from fnet_api.csrf import CSRFExemptAPIView
from openpyxl import load_workbook


class FGAPI(APIView):
    def get(self, request):
        if not request.user.is_admin:
            return Response({"error": True, "data": "Admin role required"})
        print(request.user.id)
        fg_id = request.GET.get("id")
        error = False
        if fg_id:
            try:
                queryset = FG.objects.get(id=fg_id)
                data = FGSerializer(queryset).data
            except FG.DoesNotExist:
                data = "FG does not exist"
                error = True
        else:
            queryset = FG.objects.all().order_by("-is_admin")
            data = FGSerializer(queryset, many=True).data
        return Response({"error": error, "data": data})

    def delete(self, request):
        if not request.user.is_admin:
            return Response({"error": True, "data": "Admin role required"})
        fg_id = request.GET.get("id")
        if fg_id:
            FG.objects.filter(id=fg_id).delete()
        else:
            FG.objects.all().delete()
        return Response({})

    def post(self, request):
        if not request.user.is_admin:
            return Response({"error": True, "data": "Admin role required"})
        data = request.data
        serializer = CreateFGSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if data["is_admin"] == True:
            fg = FG.objects.create_super_user(name=data["name"], 
                            student_id=data["student_id"]
                            )
        else:
            fg = FG.objects.create_user(name=data["name"], 
                            student_id=data["student_id"]
                            )

        # try:
        #     with transaction.atomic():
        #         Freshman.objects.bulk_create()
        # except IntegrityError as e:
        #     return self.Response({"data": str(e).split("\n")[1]})

        data = FGSerializer(fg).data
        
        return Response({"error": False, "data": data})
    

class FGFileUploadAPI(CSRFExemptAPIView):
    parser_classes = (MultiPartParser,)

    #TODO: 예외처리
    def post(self, request):
        if not request.user.is_admin:
            return Response({"error": True, "data": "Admin role required"})
        serializer = FGFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        error = False

        load_wb = load_workbook(file, read_only=True, data_only=True)
        load_ws = load_wb.active

        fg_info = []
        index = 0
        for row in load_ws.rows:
            if index != 0:
                row_value = []
                for cell in row:
                    row_value.append(cell.value)
                if FG.objects.filter(name=row_value[0], student_id=row_value[2]).exists():
                    continue
                fg = FG.objects.create(name=row_value[0], 
                                       student_id=row_value[2],
                                       is_admin=False)
                fg_info.append(fg)
            #header 제거
            else:
                index = 1
        # try:
        #     with transaction.atomic():
        #         Freshman.objects.bulk_create()
        # except IntegrityError as e:
        #     return self.Response({"data": str(e).split("\n")[1]})

        data = FGSerializer(fg_info, many=True).data
        return Response({"error": error, "data": data})