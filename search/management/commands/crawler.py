import requests
from bs4 import BeautifulSoup
import json
import time
import signal
from search.models import links, edges
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from search.pagerank import *
from django.db.models import Q
from django.apps import apps

class Command(BaseCommand):
	Link = apps.get_model("search", "links")

	def handle(self, *args, **options):
		extension_list_tl = {"pdf", "jpg", "png"}
		
		def is_duplicate_link(destination, source):
			if links.objects.filter(destination=destination, source=source).count() > 0:
				return True
			return False

		def get_link(id):
			try:	
				if str(id) == str(0):
					link_object = links.objects.first()
				else:
					link_object = links.objects.get(id=id)
			except Exception as e:
				print(str(e))
				return False
			return link_object

		#https://code-maven.com/python-timeout
		class TimeOutException(Exception):
			pass

		def alarm_handler(signum, frame):
			print("timeout has occured")
			raise TimeOutException()

		# from https://www.geeksforgeeks.org/python-ways-to-find-nth-occurrence-of-substring-in-a-string/
		def loc_third_slash(link):
			occurrence = 3
			inilist = [i for i in range(0, len(link)) 
					if link[i:].startswith('/')] 
			if len(inilist)>= 3:
				return inilist[occurrence-1]
			else: 
				return False

		def get_page_of_links(url, source):
			# signal.signal(signal.SIGALRM, alarm_handler)
			# signal.alarm(10)
			print("Now entering " + str(url))
			try:
				start_1 = time.time()
				page = requests.get(url)
				# print('====== Time For Request: ' + str(time.time() - start_1) + " =======")
				# signal.alarm(0)
				start_2 = time.time()
				soup = BeautifulSoup(page.content, 'html.parser')
				# print('====== Time For BS: ' + str(time.time() - start_2) + " =======")
				links_a = soup.findAll('a')
				# print(len(links_a))
			except TimeOutException as ex:
				print(ex)
				links.objects.filter(destination=url, source=source).update(visited=1)
				return
			except Exception as e:
				signal.alarm(0)
				print(str(e))
				return
			links.objects.filter(destination=url, source=source).update(visited=1)
			# print("Visited " + url)
			start_4 = time.time()
			links_to_be_saved = []
			for link in links_a:
				link_object = None
				href = link.get('href')
				if href == None:
					continue
				elif len(href) < 3:
					continue
				elif ('#' in href) or ('@' in href):
					continue
				elif (href[-3:] in extension_list_tl):
					print('FOUND FILE')
					continue
				elif (href[0:7] == 'http://' or href[0:8] == 'https://' or href[0:4] == 'www.'):
					link_object = {'destination': href, 'source': url}
					print('1')
					new_link = Link(**link_object)
					print(new_link)
					links_to_be_saved.append(new_link)
				elif (href):
					if(loc_third_slash(url)):
						new_url =  url[0:loc_third_slash(url)]
						appended_link = new_url + href
					else:
						appended_link = url + href
					link_object = {'destination': appended_link, 'source': url}
					print('2')
					new_link = Link(**link_object)
					print(new_link)
					links_to_be_saved.append(new_link)
				else:
					return
				
			# print(links_to_be_saved)
			print(str(links.objects.bulk_create(links_to_be_saved)))			
			print(time.time() - start_4)
			
	
		def save_link_to_database(link_object):
			if (is_duplicate_link(link_object['destination'], link_object['source']) == False) and (len(link_object['destination'])<399) :
				start_t1 = time.time()
				link = links.objects.create(destination=link_object['destination'], source=link_object['source'], visited = link_object['visited'])
				# print("Link post successful")
				print("t1: " + str(time.time() - start_t1))
				return link

		#global_A = numpy.zeros((2,2), float)
		# get inputs from user
		if (links.objects.first() == None):
			x = int(input("how many links do you want to seed? "))
			y = x + 1
			z = 1
			while z < y:
				link = ""
				while not (link[0:7] == 'http://' or link[0:8] == 'https://'):
					link = input("provide seed link #" + str(z) + ":")
					if not (link[0:7] == 'http://' or link[0:8] == 'https://'):
						print("NOTE: provide in http:// or https:// form")
				if (not (is_duplicate_link(link, link))):
					link_object = {'destination': link, 'source': link, 'visited': False}
					save_link_to_database(link_object)
					z = z + 1
				else:
					print(link + " is a duplicate, try again.")
		else:
			print("resuming crawl.")

		break_check = len(links.objects.filter(visited=0))
		i = links.objects.filter(visited=0).first().id
		while break_check > 0:
			start = time.time()
			link = get_link(i)
			if link:
				try:
					if not link.visited == 1:
						link.visited = True
						link.save()
						get_page_of_links(link.destination, link.source)
					else:
						print("link #" + str(i) + " was already visited. Skipping...")
				except Exception as e:
					break_check = len(links.objects.filter(visited=0))
			else:
				break_check = len(links.objects.filter(visited=0))
			i = links.objects.filter(visited=0, id__gte=(i+1)).first().id
			print(str(i) + " crawled in " + str(time.time() - start) + " seconds") 

