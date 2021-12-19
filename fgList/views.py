from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def fgList(request):
    return HttpResponse("fg list")