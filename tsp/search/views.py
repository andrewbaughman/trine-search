from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import page
from .serializers import PageSerializer
from django.forms.models import model_to_dict

from django.views import View

def index(request):
	return render(request, 'home.html')

def results(request, query):
	results = searchAlgorithm(query)
	return render(request, 'results.html', {'query':query, 'results': results,})

def searchAlgorithm(query):
	query = query.split(' ')
	results = []
	for object in query:
		print(object)
		temp_result_urls = []
		temp_result1 = page.objects.filter(title__exact=object)
		temp_result2 = page.objects.filter(title__iexact=object)
		temp_result3 = page.objects.filter(title__contains=object)
		temp_result4 = page.objects.filter(description__contains=object)
		for res in temp_result1:
			try:
				print(res.title)
				tempdata = model_to_dict(res)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))
		for res in temp_result2:
			try:
				print(res.title)
				tempdata = model_to_dict(res)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))		
		for res in temp_result3:
			try:
				print(res.title)
				tempdata = model_to_dict(res)
				if(tempdata['url'] not in temp_result_urls) and (tempdata['description'] is not ''):
					temp_result_urls.append(tempdata['url'])
					results.append(tempdata)
			except Exception as e:
				print('model to dict error: {}'.format(e))		
		for res in temp_result4:
			try:
				print(res.title)
				tempdata = model_to_dict(res)
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



class PageList(generics.ListCreateAPIView):
	queryset = page.objects.all()
	serializer_class = PageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = page.objects.all()
	serializer_class = PageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

