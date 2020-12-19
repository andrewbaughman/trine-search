from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from django.contrib.auth.models import User

from rest_framework import generics
from .models import page
from .serializers import PageSerializer, UserSerializer
from django.forms.models import model_to_dict

from django.views import View

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

class AddPage(View):
	def post(self, request):
		if request.POST.get('method') == 'is_duplicate':
			ret = {}

			url = request.POST.get('url')

			ret['is_duplicate'] = False

			webpages = page.objects.filter(url=url)
			for webpage in webpages:
				if webpage.url == url: 
					ret['is_duplicate'] = True
					return JsonResponse(ret)

			return JsonResponse(ret)
		elif request.POST.get('method') == 'add_page':	

			ret = {}

			url = request.POST.get('url')
			title = request.POST.get('title')
			description = request.POST.get('description')

			webpage = page.objects.create(url=url, title=title, description=description)

			ret['page'] = model_to_dict(webpage)

			return JsonResponse(ret)
		elif request.POST.get('method') == 'get_link':	
			ret = {}
			id = request.POST.get('id')
			if str(id) == str(0):
				print("First link")
				webpage = page.objects.first()
			else:
				print("Known link")
				webpage = page.objects.get(id=id)

			ret['page'] = model_to_dict(webpage)

			return JsonResponse(ret)



class PageList(generics.ListCreateAPIView):
	queryset = page.objects.all()
	serializer_class = PageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = page.objects.all()
	serializer_class = PageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer