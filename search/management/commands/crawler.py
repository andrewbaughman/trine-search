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
from search.crawl_utils import *
from search.readrules import *

class Command(BaseCommand):

	def handle(self, *args, **options):
		
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
					robot_crawler = Crawler(link)
					robot_crawler.crawl_sitemap()
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
					print(str(e))
					break_check = len(links.objects.filter(Q(isTrine=2) | Q(isTrine=1), visited=False))
			else:
				break_check = len(links.objects.filter(Q(isTrine=2) | Q(isTrine=1), visited=False))
			i = i + 1
			print(i)

