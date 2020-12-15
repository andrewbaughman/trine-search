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
	results = []
	for i in range(1,10):
		result = {
			'url': 'http://www.notgoogle.com',
			'title': 'NotGoogle',
			'description': 'This website is not google. Your query was: ' + query,
		}
		results.append(result)

	return results