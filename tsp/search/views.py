from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'home.html')

def results(request, query):
	results = searchAlgorithm(query)
	return render(request, 'results.html', {'results': results})

def searchAlgorithm(query):
	results = []
	for i in range(1,10):
		result = {
			'url': 'http://www.notgoogle.com',
			'title': 'NotGoogle',
			'description': 'This website is not google. Your query was: ' + query,
		}
		results.append(result)

	return results