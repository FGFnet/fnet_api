from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class CSRFExemptAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)