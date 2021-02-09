from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import page
from django.contrib.auth.models import User

from rest_framework import generics
from .models import page
from .serializers import PageSerializer, UserSerializer
from django.forms.models import model_to_dict
import networkx
import numpy

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

def rankingAlgorithm(query):
	##adds directed edges in the graph
	def add_edges(graph):
		for each in graph.nodes():
			for eachone in graph.nodes():
				if (each!=eachone):
					graph.add_edge(each, eachone)
				else:
					continue
		return graph
	##Sorting of Nodes
	def node_sort(graph, pts):
		total = numpy.array(pts)
		total = numpy.argsort(-total)
		return total
	##directed graph with n nodes
	graph = networkx.DiGraph()
	n = 10 ##need to figure out where to get number of nodes based on a search##
	graph.add_nodes_from(range(n))
	##page_dict as dictionary of tuples
	page_dict = networkx.pagerank(graph)
	for q in range(len(page_dict)):
		if page_dict[q] == query:
			page_sort = sorted(page_dict.items(), key=lambda x: x[1], reverse=True)
			return page_sort
	for i in page_sort:
		print(i[0], end="")


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

