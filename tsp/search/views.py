from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'home.html')

def results(request):
    return render(request, 'results.html')

def search(request):
    query = request.GET.get('query')
    response = {
        'results': searchAlgorithm(query),
    }
    return JsonResponse(response)


def searchAlgorithm(query):
	results = {
        'result1': query + ' will return this result and others',
        'result2': 'like me', 
    }

	return results