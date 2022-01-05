from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view
from lc.models import LC
from .models import Freshman
from .serializers import CreateFreshmanSerializer, EditFreshmanSerializer, FreshmanSerializer, FreshmanFileUploadSerializer
from django.db import transaction, IntegrityError
import csv
import io


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
                                student_id=data["student_id"],
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
    

class FreshmanFileUploadAPI(APIView):
    parser_classes = (MultiPartParser,)

    # TODO: Add exception handling
    def post(self, request):
        serializer = FreshmanFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        decoded_file = file.read().decode("utf-8-sig")
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        data_list = [row for row in reader]
        # remove header
        # data_list.pop(0)
        freshman_list = []

        for data in data_list:
            # lc_name = data[5]
            lc_name = "lc10"
            try:
                lc = LC.objects.get(name=lc_name)
            except LC.DoesNotExist:
                continue
            freshman_list.append(Freshman(lc=lc, name=data[0], department=data[1], student_id=data[2], phone_number=data[3]))
        try:
            with transaction.atomic():
                Freshman.objects.bulk_create(freshman_list)
        except IntegrityError as e:
            return self.Response({"data": str(e).split("\n")[1]})
        return Response({})


@api_view(['GET'])
def getLCMemberList(request):
    error = False
    lc_id = request.GET.get("id")
    register = request.GET.get("register")
    if not lc_id:
        data = "LC id is required"
        error = True
    else:
        queryset = Freshman.objects.filter(lc_id=lc_id, register=register)
        data = FreshmanSerializer(queryset, many=True).data
    return Response({"error": error, "data": data})