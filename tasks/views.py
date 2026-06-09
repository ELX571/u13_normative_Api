from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def salomApiView(request):
    return JsonResponse({'message':'Hello World!'})