from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, 'home.html')

def results(request):
    return render(request, 'results.html')

def testAjax(request):
    response = {
        'message': 'it worked!',
    }
    return JsonResponse(response)