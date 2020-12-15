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
        'result1': {
			'url': 'http://www.notgoogle.com',
			'title': 'NotGoogle',
			'description': 'This website is not google.',
		},
        'result2': {
			'url': 'http://www.alsonotgooel.com',
			'title': 'AlsoNotGoogle',
			'description': 'This website is also not google.',
		}, 
		'results3': {
			'url': 'http://www.'+ query +'.com',
			'title': query,
			'description': query,
		},
    }

	return results