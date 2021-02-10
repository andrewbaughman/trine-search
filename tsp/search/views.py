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
import networkx as nx
import socket

from django.views import View



def index(request):
	return render(request, 'home.html')

def results(request):
	query = request.GET.get('query')
	results = searchAlgorithm2(query)
	return render(request, 'results.html', {'query':query, 'results': results,})

def searchAlgorithm1(query):
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

def searchAlgorithm2(query):
	query = query.split(' ')
	HOST = '127.0.0.2'
	PORT = 65432

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		message = "get_ranked_list, " + str(query)
		print(message)
		s.sendall(message.encode("utf-8"))
		data = s.recv(1024).decode("utf-8")

		print(data)

class AddPage(View):
	def post(self, request):
		if request.POST.get('method') == 'add_page':	

			ret = {}

			url = request.POST.get('url')
			title = request.POST.get('title')
			description = request.POST.get('description')
			link_object = links.objects.get(destination=url)
			webpage = page.objects.create(url=link_object, title=title, description=description)

			ret['page'] = model_to_dict(webpage)

			return JsonResponse(ret)

		elif request.POST.get('method') == 'is_duplicate_page':
				ret = {}
				url = request.POST.get('url')
				link_object = links.objects.get(destination=url)
				ret['is_duplicate_page'] = False
				page_urls = page.objects.filter(url=url)
				for link in page_urls:
					if link.url == link_object: 
						ret['is_duplicate_page'] = True
						return JsonResponse(ret)
				return JsonResponse(ret)

class LinkController(View):
	def post(self, request):
			if request.POST.get('method') == 'is_duplicate_link':
				ret = {}
				destination = request.POST.get('destination')
				ret['is_duplicate_link'] = False
				destination_links = links.objects.filter(destination=destination)
				for link in destination_links:
					if link.destination == destination: 
						ret['is_duplicate_link'] = True
						return JsonResponse(ret)
				return JsonResponse(ret)

			elif request.POST.get('method') == 'add_link':	

				ret = {}

				destination = request.POST.get('destination')
				source = request.POST.get('source')
				isTrine = request.POST.get('isTrine')

				link_object = links.objects.create(destination=destination, source=source, isTrine=isTrine, visited = False)

				ret['links'] = model_to_dict(link_object)

				return JsonResponse(ret)
			elif request.POST.get('method') == 'get_keywords':
				ret = {}
				url = request.POST.get('url')
				try:
					print(url)
					link_object = links.objects.get(destination=url)
					print(link_object)
					print(keywords.objects.filter(url=link_object.id))

					ret['keyword_list'] = entities

				except:
					ret['error'] = "No link in db"

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