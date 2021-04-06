import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from search.models import *
from search.crawl_utils import *
import tldextract
import time
from django.forms.models import model_to_dict
from django.db.models import Q


class Crawler:
	def __init__(self, url):
		self.domain = self.determine_domain(url)
		self.rules_file = self.fetch_rules_file()
		self.rules = self.parse_rules()
		self.sitemap = self.parse_sitemap()
		

	def crawl_sitemap(self):
		previous = time.time()
		for site in self.sitemap:
			try:
				link = links.objects.get(destination=site)
				if not link.visited:
					visit = True
				else:
					visit = False
			except:
				visit = True
			if visit==True:
				if (not site in self.rules['disallowed']) or (site in self.rules['allowed']):					
					print("CRAWL_DELAY: " + str(self.rules['crawl_delay']))
					domains = []
					domains.append(self.domain)
					while((time.time() - previous) < float(self.rules['crawl_delay'])):
						link = links.objects.filter(~Q(destination__in=domains))[:1]
						domains.append(self.determine_domain(link.destination))
						get_page_of_links(link.destination, True)
					get_page_of_links(site, True)
					previous = time.time()
					print("Sitemap location crawled")
			
	def fetch_rules_file(self):
		robots = self.domain + "/robots.txt"
		robotrules = requests.get('http://' + robots).text
		return robotrules

	def determine_domain(self, link):
		extracted = tldextract.extract(link)
		domain = "{}.{}".format(extracted.domain, extracted.suffix)
		return domain

	def parse_rules(self):
		user_agents = []
		disallowed = []
		allowed = []
		sitemap = ""
		crawl_delay = 0

		if not "User-agent" in self.rules_file:
			print("NO ROBOTS.TXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

		lines = self.rules_file.split('\n')
		for line in lines:
			line_list = line.split(': ')
			if len(line_list) == 2:
				if line_list[0].lower() == "user-agent":
					user_agents.append(line_list[1])
				if line_list[0].lower() == "disallow":
					disallowed.append(self.domain + line_list[1])
				if line_list[0].lower() == "allow":
					allowed.append(self.domain + line_list[1])
				if line_list[0].lower() == "sitemap":
					sitemap = line_list[1]
				if line_list[0].lower() == "crawl-delay":
					crawl_delay = line_list[1]
		parsed_rules = {}
		parsed_rules['user_agents'] = user_agents
		parsed_rules['disallowed'] = disallowed
		parsed_rules['allowed'] = allowed
		parsed_rules['sitemap'] = sitemap
		parsed_rules['crawl_delay'] = crawl_delay
		return parsed_rules	

	def parse_sitemap(self):
		sites = []

		xmlpage = requests.get(self.rules['sitemap']).text
		bs = BeautifulSoup(xmlpage, 'xml')
		locs = bs.find_all('loc')
		for loc in locs:
			sites.append(loc.text)

		return sites



