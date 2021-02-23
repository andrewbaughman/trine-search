import requests
from bs4 import BeautifulSoup
import json
import time
import signal
from search.models import links
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		inclusion = {"trine", "Trine"}
		def is_duplicate_link(destination):
			destination_links = links.objects.filter(destination=destination)
			for link in destination_links:
				if link.destination == destination: 
					return True
			return False

		def add_link(linkObject):
			link_object = links.objects.create(destination=linkObject['destination'], source=linkObject['source'], isTrine=linkObject['isTrine'], visited = False)
			model_to_dict(link_object)
			return

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

		# from https://www.geeksforgeeks.org/python-ways-to-find-nth-occurrence-of-substring-in-a-string/
		def loc_third_slash(link):
			occurrence = 3
			inilist = [i for i in range(0, len(link)) 
					if link[i:].startswith('/')] 
			if len(inilist)>= 3:
				return inilist[occurrence-1]
			else: 
				return False

		def trine_url(url):
			for i in inclusion:
				if i in url:
					return True
			return False

		def get_page_of_links(url):
			signal.signal(signal.SIGALRM, alarm_handler)
			signal.alarm(10)
			print("Now entering " + url)
			try:
				page = requests.get(url)
				soup = BeautifulSoup(page.content, 'html.parser')
				links_a = soup.findAll('a')
			except TimeOutException as ex:
				print(ex)
				links.objects.filter(destination=url).update(visited=True)
				return
			signal.alarm(0)
			links.objects.filter(destination=url).update(visited=True)
			print("Visited " + url)
			for link in links_a:
				href = link.get('href')
				if href == None:
					continue
				elif href:
					if href[0:7] == 'http://' or href[0:8] == 'https://':
						link_object = {'destination': href, 'source': url, 'isTrine': trine_url(href), 'visited': False}
						save_link_to_database(link_object)
					# search for subpage of url that meets the criteria
					elif (href[0] == '/'):
						if(loc_third_slash(url)):
							url =  url[0:loc_third_slash(url)]
						appended_link = url + href
						link_object = {'destination': appended_link, 'source': url, 'isTrine': trine_url(appended_link), 'visited': False}
						save_link_to_database(link_object)
							
		def save_link_to_database(link_object):
			# check for duplicate before sending
			if is_duplicate_link(link_object['destination']) == False:
				add_link(link_object)
				print("Link post successful")

		# get inputs from user
		if (links.objects.first() == None):
			x = input("how many links do you want to seed? ")
			y = int(x) + 1
			z = 1
			while z < y:
				link = ""
				while not (link[0:7] == 'http://' or link[0:8] == 'https://'):
					link = input("provide seed link #" + str(z) + ":")
					if not (link[0:7] == 'http://' or link[0:8] == 'https://'):
						print("NOTE: provide in http:// or https:// form")
				if (not (is_duplicate_link(link))):
					link_object = {'destination': link, 'source': "", 'isTrine': trine_url(link), 'visited': False}
					save_link_to_database(link_object)
					z = z + 1
				else:
					print(link + " is a duplicate, try again.")
		else:
			print("resuming crawl.")

		i = 0
		while 1:
			link =get_link(i)
			url = link.destination
			if not link.visited:
				get_page_of_links(url)
			else:
				print("link #" + str(i) + " was already visited. Skipping...")
			i = link.id + 1
			print(i)

