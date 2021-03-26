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
from django.db.models import Sum

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
	page_searched = request.GET.get('page')
	if not page_searched:
		page_searched = 1
	page_searched = int(page_searched) - 1
	query = init_query.lower().split()
	query = parse_query(query)
	#get a ranked list of Trine pages based on keyword and important words
	ranked_list = get_ranked_list(set(query), False)
	num_results_total = len(ranked_list)
	ranked_list = ranked_list[:200]
	#set allowable results per page
	results_len = 10
	num_results = len(ranked_list)
	num_pages = int(num_results / results_len) + (num_results % results_len > 0)
	
	pages = divide_list(ranked_list, num_pages)
	page_list = make_list(num_pages)
	
	if page_searched <= num_pages:
		for source in pages[page_searched]:
			try:
				#get page info from ranked list
				link = links.objects.get(id = source)
				site = page.objects.get(url=link)
				site = model_to_dict(site)
				results.append(site)
				results_len -= 1
			except Exception as e:
				pass
		#call query correction. The decimal is for tollerance 
		correction = typo_correction(init_query.lower().split(), 0.75)
		if correction == '':
			correction = init_query
		#stop query timmer
		end = time.time()
		#return html page
		return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,'correction': correction, 'pages': page_list, 'num_results': num_results_total})
	end = time.time()
	return render(request, 'results.html', {'query':init_query, 'results': 'None', 'time':end-start,'correction': init_query, 'pages': page_list, 'num_results': num_results_total})

#get Trine results page
def trine_results(request):
	#set start time for query
	start = time.time()
	results = []
	#create initial query list
	init_query = request.GET.get('query')
	page_searched = request.GET.get('page')
	if not page_searched:
		page_searched = 1
	page_searched = int(page_searched) - 1
	query = init_query.lower().split()
	query = parse_query(query)
	#get a ranked list of Trine pages based on keyword and important words
	ranked_list = get_ranked_list(set(query), True)
	num_results_total = len(ranked_list)
	ranked_list = ranked_list[:200]
	#set allowable results per page
	results_len = 10
	num_results = len(ranked_list)
	num_pages = int(num_results / results_len) + (num_results % results_len > 0)
	
	pages = divide_list(ranked_list, num_pages)
	page_list = make_list(num_pages)
	
	if page_searched <= num_pages:
		for source in pages[page_searched]:
			try:
				#get page info from ranked list
				link = links.objects.get(id = source)
				site = page.objects.get(url=link)
				site = model_to_dict(site)
				results.append(site)
				results_len -= 1
			except Exception as e:
				pass
		#call query correction. The decimal is for tollerance 
		correction = typo_correction(init_query.lower().split(), 0.75)
		if correction == '':
			correction = init_query
		#stop query timmer
		end = time.time()
		#return html page
		return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,'correction': correction, 'pages': page_list, 'num_results': num_results_total})
	end = time.time()
	return render(request, 'results.html', {'query':init_query, 'results': 'None', 'time':end-start,'correction': init_query, 'pages': page_list, 'num_results': num_results_total})

#divide list
def divide_list(lst, n):
	if n == 0:
		return [lst]
	p = len(lst) // n
    
	if len(lst)-p > 0:
		return [lst[:p]] + divide_list(lst[p:], n-1)
	else:
		return [lst]

def make_list(size):
	returned = list()
	nume = 1
	while size > 0:
		returned.append(nume)
		nume += 1
		size -= 1
	return returned
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
	urls_to_keyword = False
	for entity in entity_list:
		#a dictionary the has 'key' and values that are 2-dimensional- one for word freqency
		# and the other for the number of important words that match the query
		#remove the last 's' of a word
		if entity[-1] == 's':
		 	entity = entity[:(len(entity) -1)]
		kwobjects =[]
		try:
			#get keyword objects
			if first_time:
				if isTrine:
					urls_to_keyword = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')) ,url__isTrine=1)
				else:
					urls_to_keyword = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')))
				first_time = False
			else:
				if isTrine:
					kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')) ,url__isTrine=1)
				else:
					kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')))
				urls_to_keyword = (urls_to_keyword | kwobjects)
		except Exception as e:
			print(str(e))
	#sort the return values based on important words, then by freqency
	if urls_to_keyword:
		returned_values = urls_to_keyword.values('url_id').annotate(important_score = Sum('is_substr'), freq_score = Sum('times_on_page')).order_by('-important_score', '-freq_score')
		print(returned_values)
		final_values = list()
		for value in returned_values:
			final_values.append(value['url_id'])
		#return the list
		return list(final_values)
	return list()


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
