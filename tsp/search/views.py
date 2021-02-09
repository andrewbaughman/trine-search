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
	G = nx.Graph()
	entities = [] ## need to acquire from the db, ever changing 

	## using sockets (example) ##
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		pass
	##						 ##

	def update_graph(entities):
		for entity in entities:
			if (entity not in G):
				G.add_node(entity)
		adjust_edges(entities)	

	def adjust_edges(entities):
		for entity in entities:
			for other_entity in entities:
				if other_entity != entity:
					if (entity in G.neighbors(other_entity)):
						G[entity][other_entity]['weight'] += 1
					else:
						G.add_edge(entity, other_entity)
						G[entity][other_entity]['weight'] = 1

	def load_graph():
		G = nx.read_gml("graph")

	def save_graph():
		nx.write_gml(G, "graph")

	def retrieve_topic(query):
		topic = {}
		for word in query:
			if G.has_node(word):
				topic[word] = 100
				neighbors = G.neighbors(word)
				for neighbor in neighbors:
					if neighbor in topic:
						topic[neighbor] += G[word][neighbor]['weight']
					else:
						topic[neighbor] = G[word][neighbor]['weight']
		return topic


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
		elif request.POST.get('method') == 'get_keywords':
			ret = {}
			url = request.POST.get('url')
			link = links.objects.filter(url=url)
			keywords = keywords.objects.filter(url=url)


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