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
from django.db.models import Q

import json
import time
import json

exception_list = ("", " ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the")

def index(request):
	return render(request, 'home.html')

def results(request):
	start = time.time()
	results = []
	init_query = request.GET.get('query')
	query = init_query.lower().split()
	query = parse_query(query)
	print(query)

	ranked_list = get_ranked_list(query, False)
	#for key in ranked_list:
	#	print(str(key) + ': ' + str(ranked_list[key]))
	success = 0
	for source in ranked_list:
		try:
			link = links.objects.get(destination=source.destination)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
			success += 1
			if success > 19:
				break
		except Exception as e:
			pass
	
	#results = searchAlgorithm(query)
	end = time.time()
	return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,})

def trine_results(request):
	start = time.time()
	results = []
	init_query = request.GET.get('query')
	query = init_query.lower().split()
	query = parse_query(query)
	ranked_list = get_ranked_list(query, True)
	#for key in ranked_list:
	#	print(str(key) + ': ' + str(ranked_list[key]))
	success = 0
	for source in ranked_list:
		try:
			link = links.objects.get(destination=source.destination)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
			success += 1
			if success > 19:
				break
		except Exception as e:
			pass
	
	#results = searchAlgorithm(query)
	end = time.time()
	query_string = ""
	for word in query:
		query_string += str(word)
		query_string += " "
	return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,})

def parse_query(query):
	for item in query:
		if item in exception_list:
			query.remove(item)
	return query

def get_ranked_list(entity_list, isTrine):
	ranked_list = {}

	# Make list of lists of urls. Each list of urls matches 1 keyword in query
	lists_of_urls = []
			
	for entity in entity_list:
		if entity[-1] == 's':
		 	entity = entity[:(len(entity) -1)]
		urls_to_keyword = []
		kwobjects =[]
		try:
			if isTrine:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')) ,url__isTrine=True).values('url')
			else:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's'))).values('url')
			urls_to_keyword = links.objects.filter(id__in=kwobjects)
			urls_to_keyword = set(url.id for url in urls_to_keyword)

		except Exception as e:
			print(str(e))
		lists_of_urls.append(urls_to_keyword)
	
	# Intersect list of lists of urls so that all that's left is urls that match all keywords
	intersected_urls = lists_of_urls[0]
	for url_list in lists_of_urls:
		intersected_urls = list(set(intersected_urls) & set(url_list))
	
	# Sort the ranked list by highest first 
	ranked_list = list(links.objects.filter(id__in=intersected_urls).order_by('pagerank'))
	#ranked_list = dict(sorted(ranked_list.items(), key=lambda item: item[1], reverse=True))
	return ranked_list


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
