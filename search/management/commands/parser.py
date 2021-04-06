import requests
from bs4 import BeautifulSoup
import json
import time
import signal
from search.models import links
from search.models import page
from search.models import keywords
from search.models import image
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from search.keywords import *
from search.crawl_utils import *

import hashlib

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		
		def matching_page(parsed_page):
			matching_page = page.objects.filter(hashId=parsed_page['hashId'])
			if matching_page.count() == 1:
				print("FOUND MATCHING PAGE")
				found = links.objects.get(destination=matching_page[0].url.destination)
				current = links.objects.get(destination=parsed_page['url'])
				if current.pagerank > found.pagerank:
					found.delete()
					print("DELETING RECORD FOR " + found.destination)
					return True
				else:
					current.delete()
					print("this matching page will not be saved.")
					return False
			elif matching_page.count() > 1:
				print("ERROR FOUND!")
			return True
				
		def save_keywords_to_database(url, __keywords):
			inclusion = {"trine", "Trine"}
			parsed_page_keywords = json.dumps(__keywords)

			### https://www.guru99.com/python-json.html
			entities = json.loads(parsed_page_keywords)
			try:
				link_object = links.objects.get(destination=url)
				page_object = page.objects.get(url=link_object)
				ls = True
				if link_object.isTrine == 1:
					ls = False
				### https://www.w3schools.com/python/gloss_python_loop_dictionary_items.asp
				for keyword in entities:
					key = keyword
					value = entities[keyword]
					important = 0
					if (key in inclusion) and ls:
						link_object.isTrine = 1
						link_object.save()
						print("ThIs SoUrCe IsTrInE!")
						ls = False
					if (key in page_object.title.lower()) or (key in link_object.destination.lower()):
						important = 1
					kwobject = keywords.objects.create(url=link_object, keyword=key, times_on_page=value, is_substr=important)
						
			except Exception as e:
				print(str(e))
				return False

		def save_page_to_database(parsed_page):	
			link_object = links.objects.get(destination=url)
			webpage = page.objects.create(url=link_object, title=parsed_page['title'], description=parsed_page['description'], hashId=parsed_page['hashId'])
			model_to_dict(webpage)
			print("Post successful !")
			return

		def is_duplicate_page(url):
				link_object = links.objects.get(destination=url)
				page_urls = page.objects.filter(url=url)
				for link in page_urls:
					if link.url == link_object: 
						return True
				return False
				
		def loc_slash_occurrence(link , occurrence):
			try:
				inilist = [i for i in range(0, len(link)) 
						if link[i:].startswith('/')]
				if len(inilist)>= occurrence:
					return inilist[occurrence-1]
				else: 
					return False
			except Exception as e:
				return False

		def get_page_info(soup):
			link_object = links.objects.get(destination=url)
			parsed_page = {}						
			if soup.find('title'):
				title = soup.find('title').get_text()
				title_trim = title
				if (len(title) > 70):
					title_trim = title[:65] + " ..."
				parsed_page['title'] = title_trim
			else:
				return False
			if soup.find("meta", {"name":"description"}):
				print('found meta description!')
				best_description = soup.find("meta", {"name":"description"})['content']
				descriptions = best_description
			elif soup.find("meta", {"name":"Description"}):
				print('found meta Description!')
				best_description = soup.find("meta", {"name":"Description"})['content']
				descriptions = best_description
			elif soup.find('p'):
				best_description = ''					
				descriptions = soup.findAll('p')
				for description in descriptions:
					description_text = description.get_text()
					if len(description_text) > len(best_description):
						best_description = description_text
			else:
				best_description = 'No description Available.'
				descriptions = best_description
			if (len(best_description) > 200):
					best_description = best_description[:195] + " ..."
			encoded_str = str(list(descriptions) + list(title)).encode()
			hash_object = hashlib.sha1(encoded_str)
			hex_dig = hash_object.hexdigest()
			parsed_page['hashId'] = hex_dig
			parsed_page['description'] = best_description
			parsed_page['url'] = url
			return parsed_page

		def save_images(soup, url):
			link_object = links.objects.get(destination=url)
			imgs = soup.find_all('img', src=True)
			for img in imgs:
				process = img['src'].split('src=')[-1]
				if ('noscript=1' not in process) and ('safelinks.pro' not in process):
					attempt = 3
					processed = process
					if (processed[0:7] == 'http://' or processed[0:8] == 'https://' or processed[0:4] == 'www.'):
						if len(processed) <= 400:
							print('saved image')
							image.objects.create(source_url=link_object, image_url=processed)
						
					else:
						#url = determine_domain(url)
						#if process[0] == '/':
						#	processed = url + process[1:]
						#else:
						#	processed = url + process
						processed = restructure_url(url, process)
						response = requests.get(processed)
						if str(response) == '<Response [200]>':
							if len(processed) <= 400:
								print('saved image')
								image.objects.create(source_url=link_object, image_url=processed)
											
		i = int(input("What id do you want to start at? (make this the same for all parser instaces) "))
		x = int(input("How many parsers are there/ do you want? "))
		y = int(input("What number parser is this? "))
		break_check = len(links.objects.filter(parsed=False))
		while break_check > 0:
			link = get_link(i + y)
			if link:
				url = link.destination
				if link.parsed:
					print("resuming...")
				elif is_duplicate_page(url):
					print("" + url + " is a duplicate page. Skipping...")
					link.parsed = True
					link.save()
				else:
					link.parsed = True
					link.save()
					print("now entering: " + url)
					signal.signal(signal.SIGALRM, alarm_handler)
					signal.alarm(10)
					try:
						__page = requests.get(url)
						soup = BeautifulSoup(__page.content, 'html.parser')
						signal.alarm(0)
						parsed_page = get_page_info(soup)
						__keywords = get_keywords(soup)
						if parsed_page and matching_page(parsed_page):
							save_page_to_database(parsed_page)
							save_images(soup, url)
							if __keywords:
								save_keywords_to_database(url, __keywords)
					except TimeOutException as ex:
						print(ex)
					except Exception as e:
						print(str(e))
						signal.alarm(0)
						break_check = len(links.objects.filter(parsed=False))
			else:
				break_check = len(links.objects.filter(parsed=False))
			i = i + x
			print(i)
