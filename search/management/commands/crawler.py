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


class Command(BaseCommand):

	def handle(self, *args, **options):
		inclusion = {"trine", "Trine"}
		extension_list_tl = {"pdf", "jpg", "png"}
		def is_duplicate_link(destination):
			destination_links = links.objects.filter(destination=destination)
			for link in destination_links:
				if link.destination == destination: 
					return True
			return False

		def add_link(linkObject):
			link_object = links.objects.create(destination=linkObject['destination'], source=linkObject['source'], isTrine=linkObject['isTrine'], visited = False)
			return link_object

		def add_edge(edgeObject):
			edge_object = edges.objects.create(pointA=edgeObject['pointA'], pointB=edgeObject['pointB'])
			return model_to_dict(edge_object)

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

		def trine_url(url):
			for i in inclusion:
				if i in url:
					return 1
			return 2
		
		def trine_url_from_not(url):
			for i in inclusion:
				if i in url:
					return 1
			return 3

		def get_page_of_links(url, trine):
			signal.signal(signal.SIGALRM, alarm_handler)
			signal.alarm(10)
			print("Now entering " + url)
			try:
				page = requests.get(url)
				signal.alarm(0)
				soup = BeautifulSoup(page.content, 'html.parser')
				links_a = soup.findAll('a')
			except TimeOutException as ex:
				print(ex)
				links.objects.filter(destination=url).update(visited=True)
				return
			except Exception as e:
				signal.alarm(0)
				print(str(e))
				return
			links.objects.filter(destination=url).update(visited=True)
			print("Visited " + url)
			for link in links_a:
				href = link.get('href')
				if href == None:
					continue
				elif len(href) < 3:
					continue
				elif (href[0] == '#'):
					continue
				elif (href[-3:] in extension_list_tl):
					print('FOUND FILE')
					continue
				elif (href[0:7] == 'http://' or href[0:8] == 'https://' or href[0:4] == 'www.'):
					if trine:
						link_object = {'destination': href, 'source': url, 'isTrine': trine_url(href), 'visited': False}
					else:
						link_object = {'destination': href, 'source': url, 'isTrine': trine_url_from_not(href), 'visited': False}
					save_link_to_database(link_object)
				elif (href):
					if(loc_third_slash(url)):
						new_url =  url[0:loc_third_slash(url)]
						appended_link = new_url + href
					else:
						appended_link = url + href
					if trine:
						link_object = {'destination': appended_link, 'source': url, 'isTrine': trine_url(appended_link), 'visited': False}
					else:
						link_object = {'destination': appended_link, 'source': url, 'isTrine': trine_url_from_not(appended_link), 'visited': False}
					save_link_to_database(link_object)
				else:
					return
			
			# Make a list of all connections just made
			try:
				source = links.objects.get(destination=url)
			except:
				source = links.objects.get(destination=(url + '/'))
			destinations = list(links.objects.filter(source=url))
			
			# Prep lists and generate pageranks
			_links = [source] + destinations
			_edges = edges.objects.filter(pointA=source)
			
			pageranks = PR_from_db(_edges, _links, len(_links))
			print(pageranks)

			# Save to database
			for key in pageranks:
				link = links.objects.get(id=key)
				link.pagerank = pageranks[key]
				link.save()
	
		def save_link_to_database(link_object):
			# check for duplicate before sending
			if (is_duplicate_link(link_object['destination']) == False) and (len(link_object['destination'])<399) :
				link = add_link(link_object)
				try:
					edge_object = {'pointA': links.objects.get(destination=link.source), 'pointB': link}
				except:
					print(link.source)
					edge_object = {'pointA': links.objects.get(destination=link.source + '/'), 'pointB': link}
				add_edge(edge_object)
				print("Link post successful")
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
				if (not (is_duplicate_link(link))):
					link_object = {'destination': link, 'source': link, 'isTrine': trine_url(link), 'visited': False}
					save_link_to_database(link_object)
					z = z + 1
				else:
					print(link + " is a duplicate, try again.")
		else:
			print("resuming crawl.")

		break_check = len(links.objects.filter(visited=False))
		i = 0
		while break_check > 0:
			link =get_link(i)
			if link:
				try:
					url = link.destination
					if not link.visited and link.isTrine == 1:
						get_page_of_links(url, True)
					elif not link.visited and link.isTrine == 2:
						get_page_of_links(url, False)
					elif not link.visited and link.isTrine == 3:
						print("link #" + str(i) + " is too far away, will not crawl...")
					else:
						print("link #" + str(i) + " was already visited. Skipping...")
				except Exception as e:
					break_check = len(links.objects.filter(Q(isTrine=2) | Q(isTrine=1), visited=False))
			else:
				break_check = len(links.objects.filter(Q(isTrine=2) | Q(isTrine=1), visited=False))
			i = i + 1
			print(i)

