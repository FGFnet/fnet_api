from fg.models import FG
from fg.serializers import (FGSerializer, FGFileUploadSerializer)
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.db import transaction, IntegrityError

from openpyxl import load_workbook


class FGAPI(APIView):
    def get(self, request):
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
            queryset = FG.objects.all().order_by("-admin")
            data = FGSerializer(queryset, many=True).data
        return Response({"error": error, "data": data})

    def delete(self, request):
        fg_id = request.GET.get("id")
        if fg_id:
            FG.objects.filter(id=fg_id).delete()
        else:
            FG.objects.all().delete()
        return Response({})
    

class FGFileUploadAPI(APIView):
    parser_classes = (MultiPartParser,)

    #TODO: 예외처리
    def post(self, request):
        serializer = FGFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        error = False

        load_wb = load_workbook(file, read_only=True, data_only=True)
        load_ws = load_wb['Sheet1']

        fg_info = []
        index = 0
        for row in load_ws.rows:
            if index != 0:
                row_value = []
                for cell in row:
                    row_value.append(cell.value)
                fg = FG.objects.create(name=row_value[0], 
                                    student_id=row_value[1],
                                    admin=row_value[2])
                fg_info.append(fg)
            #header 제거
            else:
                index = 1
        try:
            with transaction.atomic():
                Freshman.objects.bulk_create(freshman_list)
        except IntegrityError as e:
            return self.Response({"data": str(e).split("\n")[1]})

        data = FGSerializer(fg_info, many=True).data
        return Response({"error": error, "data": data})