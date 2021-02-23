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

import time


def index(request):
	return render(request, 'home.html')

def results(request):
	start = time.time()
	results = []
	query = request.GET.get('query').split(' ')
	ranked_list = get_ranked_list(query)
	for key in ranked_list:
		print(str(key) + ': ' + str(ranked_list[key]))
	for source in ranked_list:
		try:
			link = links.objects.get(destination=source)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
		except Exception as e:
			print(str(e))
	
	#results = searchAlgorithm(query)
	end = time.time()
	return render(request, 'results.html', {'query':query, 'results': results, 'time':end-start,})

def get_ranked_list(entity_list):
	ranked_list = {}

	# Make list of lists of urls. Each list of urls matches 1 keyword in query
	lists_of_urls = []
	for entity in entity_list:
		urls_to_keyword = []
		try:
			kwobjects = keywords.objects.filter(keyword=entity)
			for kwobject in kwobjects:
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
	ranked_list = dict(sorted(ranked_list.items(), key=lambda item: item[1], reverse=True))
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
			
			elif request.POST.get('method') == 'add_keywords':
				ret = {}
				url = request.POST.get('url')
				### https://www.guru99.com/python-json.html
				entities = json.loads(request.POST.get('keywords'))
				try:
					print(url)
					link_object = links.objects.get(destination=url)
					print(link_object)
					print(entities)
					### https://www.w3schools.com/python/gloss_python_loop_dictionary_items.asp
					for keyword in entities:
						key = keyword
						value = entities[keyword]
						kwobject = keywords.objects.create(url=link_object, keyword=key, times_on_page=value)
						
					ret['status'] = "OK"

				except Exception as e:
					ret['status'] = "error"
					print(str(e))

				return JsonResponse(ret)

			elif request.POST.get('method') == 'get_keywords':
				ret = {}
				url = request.POST.get('url')
				try:
					print(url)
					link_object = links.objects.get(source=url)
					print(link_object)
					print(keywords.objects.filter(url=link_object))

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
	pagination.PageNumberPagination.page_size = 8000
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
