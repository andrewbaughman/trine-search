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
from difflib import SequenceMatcher

import json
import time
import json

#standard list of values to exclude weight from when making a search
exception_list = ("", " ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the")

#Base site
def index(request):
	return render(request, 'home.html')

#get general results page
def results(request):
	#set start time for query
	start = time.time()
	results = []
	#create initial query list
	init_query = request.GET.get('query')
	query = init_query.lower().split()
	query = parse_query(query)
	#get a ranked list based on keyword and important words
	ranked_list = get_ranked_list(set(query), False)
	#set allowable results per page
	results_len = 20
	for source in ranked_list:
		try:
			#get page info from ranked list
			link = links.objects.get(id = source)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
			results_len -= 1
			#stop showing results
			if results_len == 0:
				break
		except Exception as e:
			pass
	#call query correction. The decimal is for tollerance 
	correction = typo_correction(init_query.lower().split(), 0.75)
	if correction == '':
		correction = init_query
	#stop query timmer
	end = time.time()
	#return html page
	return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,'correction': correction,})

#get Trine results page
def trine_results(request):
	#set start time for query
	start = time.time()
	results = []
	#create initial query list
	init_query = request.GET.get('query')
	query = init_query.lower().split()
	query = parse_query(query)
	#get a ranked list of Trine pages based on keyword and important words
	ranked_list = get_ranked_list(set(query), True)
	#set allowable results per page
	results_len = 20
	for source in ranked_list:
		try:
			#get page info from ranked list
			link = links.objects.get(id = source)
			site = page.objects.get(url=link)
			site = model_to_dict(site)
			results.append(site)
			results_len -= 1
			#stop showing results
			if results_len == 0:
				break
		except Exception as e:
			pass
	#call query correction. The decimal is for tollerance 
	correction = typo_correction(init_query.lower().split(), 0.75)
	if correction == '':
		correction = init_query
	#stop query timmer
	end = time.time()
	#return html page
	return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,'correction': correction,})

#remove words that appear in the exception list
def parse_query(query):
	groomed_query = []
	for item in query:
		if item not in exception_list:
			groomed_query.append(item)
	return groomed_query

#return a suggested correction of a query
def typo_correction(query_tc, closeness):
	suggestion = []
	
	#loop through each item in the query
	for i in range(len(query_tc)):
		#don't change the items in the exclusion list
		if query_tc[i] in exception_list:
			suggestion.append(query_tc[i])
		else:
			possibles = {}
			#the next two line help limit the number of keywords returned
			# the suggest term should be between 133% and 67% of the query term length
			length = len(query_tc[i])
			variability = int((length)/3)
			#get all keywords match the criteria
			values_of = keywords.objects.filter(keyword__startswith=query_tc[i][:1], word_len__gte=length-variability, word_len__lte=length+variability).distinct().values_list('keyword', flat=True)
			for kw in values_of:
				value = SequenceMatcher(None, query_tc[i], kw).ratio()
				#check to see if the suggested term is within the tollerance
				if value > closeness:
					if value == 1:
						#if the term is found, stop
						possibles[value] = kw
						break
					possibles[value] = kw
			#sort the possibilities to find best term
			possibles_sorted = sorted(possibles.items(), key=lambda item: item[0], reverse=True)
			#form query suggestion
			try:
				suggestion.append(possibles_sorted[0][1])
			except IndexError:
				pass

	## Reference: https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
	correction = ' '.join([str(elem) for elem in suggestion]) 
	#return corrected query as string
	return correction

#get the ranked list based on a query and whether the user wants only Trine results
def get_ranked_list(entity_list, isTrine):
	# Make list of lists of urls. Each list of urls matches 1 keyword in query
	returned_values = {}
	#value used to ballence the weight of each search term so that one isn't too weighted
	factor = len(entity_list)
	#used to create limit the returned results
	first_time = True
	#cycle through search terms
	for entity in entity_list:
		#a dictionary the has 'key' and values that are 2-dimensional- one for word freqency
		# and the other for the number of important words that match the query
		urls_to_keyword = {}
		#remove the last 's' of a word
		if entity[-1] == 's':
		 	entity = entity[:(len(entity) -1)]
		kwobjects =[]
		try:
			#get keyword objects
			if isTrine:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')) ,url__isTrine=1).values()
			else:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's'))).values()
			#total up important words
			for urls in kwobjects:
				vitals = 0
				if urls['is_substr']:
					vitals = 1
				if urls['url_id'] in urls_to_keyword:
					if urls_to_keyword[urls['url_id']][1] == 0:
						urls_to_keyword[urls['url_id']][1] += vitals
				else:
					urls_to_keyword[urls['url_id']] = [urls['times_on_page'], vitals]
			
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
				if key not in returned_values and first_time:
					returned_values[key] = [(value[0] / factor), urls_to_keyword[key][1]]
			#aknowledge first time looped
			first_time = False
		except Exception as e:
			print(str(e))
	#sort the return values based on important words, then by freqency
	returned_values = dict(sorted(returned_values.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True))
	returned_values = list(returned_values.keys())
	#return the list
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
	pagination.PageNumberPagination.page_size = 10
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class KeywordsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = keywords.objects.all()
	serializer_class = KeywordsSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
