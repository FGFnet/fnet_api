from fg.models import FG
from fg.serializers import FGSerializer, FGLoginSerializer

from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response

class FGAPI(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": True, "data": "login required"})
        print(request.GET.get('id'))
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
        