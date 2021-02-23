import requests
from bs4 import BeautifulSoup
import json
import time
import signal
from search.models import links
from search.models import page
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

class Command(BaseCommand):
	
	def handle(self, *args, **options):

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

		def get_page_info(url):
			parsed_page = {}
			signal.signal(signal.SIGALRM, alarm_handler)
			signal.alarm(10)
			try:
				page = requests.get(url)
				soup = BeautifulSoup(page.content, 'html.parser')
			except TimeOutException as ex:
				print(ex)
				return False
			signal.alarm(0)

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
				parsed_page = get_page_info(url)
				if parsed_page:
					save_page_to_database(parsed_page)
			i = link.id + 1
			print(i)