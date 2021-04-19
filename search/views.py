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
from django.db.models import Sum, Max
from random import *

import json
import time

#standard list of values to exclude weight from when making a search
exception_list = ("", " ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the")

#Base site
def index(request):
	return render(request, 'home.html')

#get results
def results(request):
	#set start time for query
	start = time.time()
	results = []
	#create initial query list
	init_query = request.GET.get('query')
	page_searched = request.GET.get('page')
	trine_only = (request.GET.get('isTrine') == 'True')
	lucky = (request.GET.get('lucky')=='True')
	random = (request.GET.get('random')=='True')
	query = init_query.lower().replace('”', '"').replace('“', '"').split()
	start_quoting = False
	index = 0
	for word in query:
		if word.replace('"','') == '':
			query[index] = 'a'
		elif word[0] == '"' and word[-1] != '"':
			query[index] = word + '"'
			start_quoting = True
		elif word[0] != '"' and word[-1] == '"':
			query[index] = '"' + word
			start_quoting = False
		elif word[0] == '"' and word[-1] == '"':
			pass
		elif start_quoting:
			query[index] = '"' + word + '"'
		index += 1
	query = parse_query(query)
	#get a ranked list of Trine pages based on keyword and important words
	if not random: 
		ranked_list = get_ranked_list(set(query), trine_only)
	else:
		ranked_list = get_random_page()
	num_results_total = len(ranked_list)
	ranked_list = ranked_list[:200]
	#set allowable results per page
	results_len = 10
	num_results = len(ranked_list)
	num_pages = int(num_results / results_len) + (num_results % results_len > 0)
	
	pages = divide_list(ranked_list, num_pages)
	page_list = make_list(num_pages)
	if not page_searched:
		page_searched = 1
	elif int(page_searched) not in page_list:
		page_searched = 1
	page_searched = int(page_searched) - 1
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
	correction = typo_correction(init_query.lower().replace('"','').split(), 0.75)
	if (correction == '') or (correction.split() == init_query.lower().replace('"','').split()):
		correction = init_query
	#stop query timmer
	end = time.time()
	#return html page
	return render(request, 'results.html', {'query':init_query, 'results': results, 'time':end-start,'correction': correction, 'pages': page_list, 'num_results': num_results_total, 'trine_only': trine_only, 'lucky': lucky})
	
#divide list
def divide_list(lst, n):
	if n == 0:
		return [lst]
	p = len(lst) // n
    
	if len(lst)-p > 0:
		return [lst[:p]] + divide_list(lst[p:], n-1)
	else:
		return [lst]

def get_random_page():
	maximum = links.objects.aggregate(Max('id'))['id__max']
	if len(page.objects.all()) == 0:
		return list()
	while True:
		random_id = randint(0, maximum)
		results = []
		try:
			site = links.objects.get(id=random_id)
			random_result = page.objects.get(url=site)
			results.append(site.id)
			return results
		except Exception as e:
			pass
	return list()

#make list for pagination
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
		if entity[-1] == 's':
		 	entity = entity[:(len(entity) -1)]
		exact = False
		if entity[0] == '"':
			entity = entity[1:-1]
			exact = True
		#a dictionary the has 'key' and values that are 2-dimensional- one for word freqency
		# and the other for the number of important words that match the query
		#remove the last 's' of a word
		kwobjects =[]
		try:
			#get keyword objects
			if first_time:
				if isTrine and exact:
					urls_to_keyword = keywords.objects.filter(keyword=entity ,url__isTrine=1)
				elif isTrine:
					urls_to_keyword = keywords.objects.filter(keyword=entity ,url__isTrine=1)
					urls_to_keyword = urls_to_keyword | keywords.objects.filter(keyword=(entity + 's') ,url__isTrine=1).exclude(url_id__in= urls_to_keyword.values_list('url_id'))
				elif exact:
					urls_to_keyword = keywords.objects.filter(keyword=entity)
				else:
					urls_to_keyword = keywords.objects.filter(keyword=entity)
					urls_to_keyword = urls_to_keyword | keywords.objects.filter(keyword=(entity + 's')).exclude(url_id__in= urls_to_keyword.values_list('url_id', flat=True))
				first_time = False
			else:
				if isTrine and exact:
					kwobjects = keywords.objects.filter(keyword=entity ,url__isTrine=1)
				elif isTrine:
					kwobjects = keywords.objects.filter(keyword=entity ,url__isTrine=1)
					kwobjects = kwobjects | keywords.objects.filter(keyword=(entity + 's') ,url__isTrine=1).exclude(url_id__in= kwobjects.values_list('url_id', flat=True))
				elif exact:
					kwobjects = keywords.objects.filter(eyword=entity)
				else:
					kwobjects = keywords.objects.filter(keyword=entity)
					kwobjects = kwobjects | keywords.objects.filter(keyword=(entity + 's')).exclude(url_id__in= kwobjects.values_list('url_id', flat=True))

				urls_to_keyword = (urls_to_keyword | kwobjects)
		except Exception as e:
			pass
	#sort the return values based on important words, then by freqency
	if urls_to_keyword:
		returned_values = urls_to_keyword.values('url_id').annotate(important_score = Sum('is_substr'), freq_score = Sum('times_on_page')).order_by('-important_score', '-freq_score')
		final_values = list()
		for value in returned_values:
			final_values.append(value['url_id'])
		#return the list
		return final_values
	return list()

def image_results(request):
	#set start time for query
	lucky = False
	random = False
	start = time.time()
	total_results = []
	results = []
	#create initial query list
	init_query = request.GET.get('query')
	page_searched = request.GET.get('page')
	query = init_query.lower().replace('”', '').replace('“', '').replace('"', '').split()
	query = parse_query(query)
	#get a ranked list of Trine pages based on keyword and important words
	ranked_list = get_ranked_images(set(query))
	ranked_list = ranked_list[:200]

	for source in ranked_list:
			try:
				#get page info from ranked list
				link = links.objects.get(id = source)
				images = image.objects.filter(source_url=link)
				for img in images:
					site = model_to_dict(img)
					total_results.append(site)
			except Exception as e:
				pass

	#set allowable results per page
	results_len = 50
	num_results = len(total_results)
	num_pages = int(num_results / results_len) + (num_results % results_len > 0)
	
	pages = divide_list(total_results, num_pages)
	page_list = make_list(num_pages)
	if not page_searched:
		page_searched = 1
	elif int(page_searched) not in page_list:
		page_searched = 1
	page_searched = int(page_searched) - 1
	for result in pages[page_searched]:
		results.append(result)
	#call query correction. The decimal is for tollerance 
	correction = typo_correction(init_query.lower().split(), 0.75)
	if correction == '' or (correction.split() == init_query.lower().replace('”', '').replace('“', '').replace('"', '').split()):
		correction = init_query
	#stop query timmer
	end = time.time()
	#return html page
	return render(request, 'images.html', {'query':init_query, 'results': results, 'time':end-start,'correction': correction, 'pages': page_list, 'num_results': num_results, 'lucky': lucky})

def get_ranked_images(entity_list):
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
				urls_to_keyword = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')))
				first_time = False
			else:
				kwobjects = keywords.objects.filter(Q(keyword=entity) | Q(keyword=(entity + 's')))
				urls_to_keyword = (urls_to_keyword | kwobjects)
		except Exception as e:
			pass
	#sort the return values based on important words, then by freqency
	if urls_to_keyword:
		returned_values = urls_to_keyword.values('url_id').annotate(important_score = Sum('is_substr'), freq_score = Sum('times_on_page')).order_by('-important_score', '-freq_score')
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

class ImageList(generics.ListCreateAPIView):
	queryset = image.objects.all()
	serializer_class = ImageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = image.objects.all()
	serializer_class = ImageSerializer
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