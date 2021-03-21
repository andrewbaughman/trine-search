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
			link = links.objects.get(id = source)
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
			link = links.objects.get(id = source)
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
	returned_values = {}
	factor = len(entity_list)
	times_fored = 1
	for entity in entity_list:
		urls_to_keyword = {}
		rank_to_keyword = {}
		if entity[-1] == 's':
		 	entity = entity[:(len(entity) -1)]
		kwobjects =[]
		try:
			if isTrine:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')) ,url__isTrine=True).values()
			else:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's'))).values()
			
			#the_rank = links.objects.filter(id__in=kwobjects.values('url_id')).values()

			# for item in the_rank:
			# 	rank_to_keyword[item['id']] = item['pagerank']

			for urls in kwobjects:
				vitals = 0
				if urls['is_substr']:
					vitals = 1
				if urls['url_id'] in urls_to_keyword:
					if urls_to_keyword[urls['url_id']][1] == 0:
						urls_to_keyword[urls['url_id']][1] += vitals
				else:
					urls_to_keyword[urls['url_id']] = [urls['times_on_page'], vitals]
			
			# if not isTrine:
			# 	for key in rank_to_keyword:
			# 		if key in urls_to_keyword:
			# 			remove_var = urls_to_keyword[key]
			# 			urls_to_keyword[key] = urls_to_keyword[key] * (float(rank_to_keyword[key]))
			# 			print(str(urls_to_keyword[key])+ " was " + str(remove_var))

			#add to the values to return dictionary
			for key, value in returned_values.items():
				if key in urls_to_keyword:
					# ratio to ensure that one term doesn't take over the search
					cal = value[0] / urls_to_keyword[key][0]
					if cal > 1:
						cal = 1 / cal
					returned_values[key][0] = (value[0] + urls_to_keyword[key][0] * cal)
					returned_values[key][1] = (value[1] + urls_to_keyword[key][1])
			#add new values to the return dictionary
			for key, value in urls_to_keyword.items():
				#effectively intersects with first
				if key not in returned_values and times_fored == 1:
					returned_values[key] = [(value[0] / factor), urls_to_keyword[key][1]]
			times_fored += 1
		except Exception as e:
			print(str(e))
	#sort the return values based on highest value
	returned_values = dict(sorted(returned_values.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True))
	print(returned_values)
	returned_values = list(returned_values.keys())

	return returned_values


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
	pagination.PageNumberPagination.page_size = 10000
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class KeywordsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = keywords.objects.all()
	serializer_class = KeywordsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
