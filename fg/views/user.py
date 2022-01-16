from ..models import FG
from ..serializers import FGSerializer, FGLoginSerializer, UserInfoSerializer

from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class FGAPI(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": True, "data": "login required"})

        fg_id = request.GET.get("id")
        if not fg_id:
            fg_id = request.user.id
        if fg_id:
            try:
                fg = FG.objects.get(id=fg_id)
                data = FGSerializer(fg).data
            except FG.DoesNotExist:
                data = "FG does not exist"
                error = True
        else:
            data = "Invalid parameter, id is required."
            error = True
        return Response({"error": False, "data": data})


class FGLoginAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        data = request.data
        serializer = FGLoginSerializer(data = data)
        serializer.is_valid(raise_exception=True)

        fg = auth.authenticate(name=data["name"], password=data["password"])
        
        if not fg:
            return Response({ "error": True, "data": "Invalid name or student id" })
        auth.login(request, fg)

        return Response({ "error": False, "data": "Login Succeeded" })
 
class FGLogoutAPI(APIView):
    def get(self, request):
        auth.logout(request)
        return Response({ "error": False, "data": "Logout Succeeded" })


@api_view(['GET'])
def getUserInfo(request):
    user = request.user
    if not user.is_authenticated:
        return Response({ "error": True, "data": "Invalid access" })
    return Response({"error": False, "data": UserInfoSerializer(user).data})