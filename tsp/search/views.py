from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions, pagination
from .models import page
from django.contrib.auth.models import User
from rest_framework import generics
from .models import *
from .serializers import *
from django.forms.models import model_to_dict
from django.views import View

import json
import time
import json


def index(request):
	return render(request, 'home.html')

def results(request):
	start = time.time()
	results = []
	query = request.GET.get('query').lower().split(' ')
	ranked_list = get_ranked_list(query, False)
	#for key in ranked_list:
	#	print(str(key) + ': ' + str(ranked_list[key]))
	for source in ranked_list:
		try:
			link = links.objects.get(destination=source.destination)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
		except Exception as e:
			print(str(e))
	
	#results = searchAlgorithm(query)
	end = time.time()
	return render(request, 'results.html', {'query':query, 'results': results, 'time':end-start,})

def trine_results(request):
	start = time.time()
	results = []
	query = request.GET.get('query').lower().split(' ')
	ranked_list = get_ranked_list(query, True)
	#for key in ranked_list:
	#	print(str(key) + ': ' + str(ranked_list[key]))
	for source in ranked_list:
		try:
			link = links.objects.get(destination=source.destination)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
		except Exception as e:
			print(str(e))
	
	#results = searchAlgorithm(query)
	end = time.time()
	query_string = ""
	for word in query:
		query_string += str(word)
		query_string += " "
	print(query_string)
	return render(request, 'results.html', {'query':query_string, 'results': results, 'time':end-start,})


def get_ranked_list(entity_list, isTrine):
	ranked_list = {}

	# Make list of lists of urls. Each list of urls matches 1 keyword in query
	lists_of_urls = []
	if isTrine == True:
		Trinekwds = keywords.objects.filter(keyword='trine')
		Trine = []
		for kwd in Trinekwds:
			Trine.append(kwd.url)
			
	for entity in entity_list:
		urls_to_keyword = []
		try:
			kwobjects = keywords.objects.filter(keyword=entity)[:20]
			for kwobject in kwobjects:
				if isTrine == True:
					if kwobject.url in Trine:
						link = links.objects.get(destination=kwobject.url.destination)
						urls_to_keyword.append(link.destination)
					else:
						pass
				else:
					link = links.objects.get(destination=kwobject.url.destination)
					urls_to_keyword.append(link.destination)

		except Exception as e:
			print(str(e))
		lists_of_urls.append(urls_to_keyword)
	
	# Intersect list of lists of urls so that all that's left is urls that match all keywords
	intersected_urls = lists_of_urls[0]
	for url_list in lists_of_urls:
		intersected_urls = list(set(intersected_urls) & set(url_list))
	
	# Add ranks to the intersected list
	for destination in intersected_urls:
		link = links.objects.get(destination=destination)
		ranked_list[destination] = 0
		for entity in entity_list:
			ranked_list[destination] += keywords.objects.get(url=link, keyword=entity).times_on_page
	
	# Sort the ranked list by highest first 
	print(intersected_urls)
	ranked_list = list(links.objects.filter(destination__in=intersected_urls).order_by('pagerank'))
	#ranked_list = dict(sorted(ranked_list.items(), key=lambda item: item[1], reverse=True))
	return ranked_list

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


class EdgesList(generics.ListCreateAPIView):
	queryset = edges.objects.all()
	serializer_class = EdgesSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EdgesDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = edges.objects.all()
	serializer_class = EdgesSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)




class KeywordsList(generics.ListCreateAPIView):
	queryset = keywords.objects.all()
	serializer_class = KeywordsSerializer
	pagination.PageNumberPagination.page_size = 100
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class KeywordsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = keywords.objects.all()
	serializer_class = KeywordsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
