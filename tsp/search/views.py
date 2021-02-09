from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import page
from django.contrib.auth.models import User

from rest_framework import generics
from .models import *
from .serializers import *
from django.forms.models import model_to_dict

from django.views import View

def index(request):
	return render(request, 'home.html')

def results(request):
	query = request.GET.get('query')
	results = searchAlgorithm(query)
	return render(request, 'results.html', {'query':query, 'results': results,})

def searchAlgorithm(query):
	query = query.split(' ')
	results = []
	for word in query:
		print(word)
		temp_result_urls = []
		temp_result1 = page.objects.filter(title__exact=word)
		temp_result2 = page.objects.filter(title__iexact=word)
		temp_result3 = page.objects.filter(title__contains=word)
		temp_result4 = page.objects.filter(description__contains=word)
		for result in temp_result1:
			try:
				print(result.title)
				tempdata = model_to_dict(result)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))
		for result in temp_result2:
			try:
				print(result.title)
				tempdata = model_to_dict(result)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))		
		for result in temp_result3:
			try:
				print(result.title)
				tempdata = model_to_dict(result)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))		
		for result in temp_result4:
			try:
				print(result.title)
				tempdata = model_to_dict(result)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))
	#webpages = page.objects.all()
	#for webpage in webpages:
	#	results.append(model_to_dict(webpage))
	print(len(temp_result_urls))
	return results

class AddPage(View):
	def post(self, request):
		if request.POST.get('method') == 'is_duplicate':
			ret = {}

			url = request.POST.get('url')

			ret['is_duplicate'] = False

			webpages = page_results.objects.filter(url=url)
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

			webpage = page_results.objects.create(url=url, title=title, description=description)

			ret['page_results'] = model_to_dict(webpage)

			return JsonResponse(ret)
		elif request.POST.get('method') == 'get_link':	
			ret = {}
			id = request.POST.get('id')
			if str(id) == str(0):
				print("First link")
				webpage = links.objects.first()
			else:
				print("Known link")
				webpage = links.objects.get(id=id)

			ret['links'] = model_to_dict(webpage)

			return JsonResponse(ret)

class LinkController(View):
	def post(self, request):
			if request.POST.get('method') == 'is_duplicate_link':
				ret = {}
				destination = request.POST.get('destination')
				ret['is_duplicate_link'] = False
				links = links.objects.filter(destination=destination)
				for link in links:
					if link.destination == destination: 
						ret['is_duplicate_link'] = True
						return JsonResponse(ret)
				return JsonResponse(ret)

			elif request.POST.get('method') == 'add_link':	

				ret = {}

				destination = request.POST.get('destination')
				source = request.POST.get('source')
				isTrine = request.POST.get('isTrine')

				link_object = links.objects.create(destination=destination, source=source, isTrine=description, visited = False)

				ret['links'] = model_to_dict(link_object)

				return JsonResponse(ret)

			elif request.POST.get('method') == 'get_link':	
				ret = {}
				id = request.POST.get('id')
				if str(id) == str(0):
					print("First link")
					link_object = links.objects.first()
				else:
					print("Known link")
					link_object = links.objects.get(id=id)

				ret['links'] = model_to_dict(link_object)

				return JsonResponse(ret)

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class PageList(generics.ListCreateAPIView):
	queryset = page.objects.all()
	serializer_class = PageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = page.objects.all()
	serializer_class = PageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class LinksList(generics.ListCreateAPIView):
	queryset = links.objects.all()
	serializer_class = LinksSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class LinksDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = links.objects.all()
	serializer_class = LinksSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class KeywordsList(generics.ListCreateAPIView):
	queryset = keywords.objects.all()
	serializer_class = KeywordsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class KeywordsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = keywords.objects.all()
	serializer_class = KeywordsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageResultsList(generics.ListCreateAPIView):
	queryset = page_results.objects.all()
	serializer_class = PageResultsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageResultsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = page_results.objects.all()
	serializer_class = PageResultsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)