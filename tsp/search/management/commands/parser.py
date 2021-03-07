import requests
from bs4 import BeautifulSoup
import json
import time
import signal
from search.models import links
from search.models import page
from search.models import keywords
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from search.keywords import *

class Command(BaseCommand):
	
	def handle(self, *args, **options):

		def save_keywords_to_database(url, __keywords):
			parsed_page_keywords = json.dumps(__keywords)

			### https://www.guru99.com/python-json.html
			entities = json.loads(parsed_page_keywords)
			try:
				link_object = links.objects.get(destination=url)
				### https://www.w3schools.com/python/gloss_python_loop_dictionary_items.asp
				for keyword in entities:
					key = keyword
					value = entities[keyword]
					kwobject = keywords.objects.create(url=link_object, keyword=key, times_on_page=value)
						
			except Exception as e:
				print(str(e))
				return False

			print("Post successful")


		def save_page_to_database(parsed_page):	
			link_object = links.objects.get(destination=url)
			webpage = page.objects.create(url=link_object, title=parsed_page['title'], description=parsed_page['description'])
			model_to_dict(webpage)
			print("Success")
			return

		def is_duplicate_page(url):
				link_object = links.objects.get(destination=url)
				page_urls = page.objects.filter(url=url)
				for link in page_urls:
					if link.url == link_object: 
						return True
				return False
		
		def get_link(id):	
			if str(id) == str(0):
				link_object = links.objects.first()
			else:
				link_object = links.objects.get(id=id)
			return link_object
		
		#https://code-maven.com/python-timeout
		class TimeOutException(Exception):
			pass

		def alarm_handler(signum, frame):
			print("timeout has occured")
			raise TimeOutException()

		def get_page_info(soup):
			parsed_page = {}

			if soup.find('title'):
				title = soup.find('title').get_text()
				parsed_page['title'] = title
			else:
				return False
			
			if soup.find("meta", {"name":"description"}):
				print('found meta description!')
				best_description = soup.find("meta", {"name":"description"})['content']
			elif soup.find("meta", {"name":"Description"}):
				print('found meta Description!')
				best_description = soup.find("meta", {"name":"Description"})['content']
			elif soup.find('p'):
				best_description = ''					
				descriptions = soup.findAll('p')
				for description in descriptions:
					description_text = soup.find('p').get_text()
					if len(description_text) > len(best_description):
						best_description = description_text
				parsed_page['description'] = descriptions[0].get_text()
			else:
				best_description = 'No description Available.'
			parsed_page['description'] = best_description

			parsed_page['url'] = url
			return parsed_page

			
		i = 0
		while 1:
			link = get_link(i)
			url = link.destination
			if is_duplicate_page(url):
				print("" + url + " is a duplicate page. Skipping...")
			else:
				print("now entering: " + url)
				signal.signal(signal.SIGALRM, alarm_handler)
				signal.alarm(10)
				try:
					__page = requests.get(url)
					soup = BeautifulSoup(__page.content, 'html.parser')
					signal.alarm(0)
					parsed_page = get_page_info(soup)
					__keywords = get_word_frequency(soup)
					if parsed_page:
						save_page_to_database(parsed_page)
					if __keywords:
						save_keywords_to_database(url, __keywords)
				except TimeOutException as ex:
					print(ex)
				except Exception as e:
					print(str(e))
			i = link.id + 1
			print(i)
