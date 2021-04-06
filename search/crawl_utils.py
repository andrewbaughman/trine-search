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
import tldextract

inclusion = {"trine", "Trine"}
extension_list_tl = {"pdf", "jpg", "png", "docx", "doc", "gif"}

def is_duplicate_link(destination):
	destination_links = links.objects.filter(destination=destination)
	for link in destination_links:
		if link.destination == destination: 
			return True
	return False

def add_link(linkObject):
	if str(linkObject['destination'])[-3] in extension_list_tl:
		print("||||||||||||||||||")
		return False
	else:
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
		return link_object
	except Exception as e:
		return False

#https://code-maven.com/python-timeout
class TimeOutException(Exception):
	pass

def alarm_handler(signum, frame):
	print("timeout has occured")
	raise TimeOutException()

def determine_domain(link):
		extracted = tldextract.extract(link)
		domain = "{}.{}".format(extracted.domain, extracted.suffix)
		return domain

def restructure_url(url, href):
	if href[0] != '/':
		href = '/' + href
	return "http://" + determine_domain(url) + href

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
		elif ('#' in href) or ('@' in href):
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
			appended_link = restructure_url(url, href)
			if trine:
				link_object = {'destination': appended_link, 'source': url, 'isTrine': trine_url(appended_link), 'visited': False}
			else:
				link_object = {'destination': appended_link, 'source': url, 'isTrine': trine_url_from_not(appended_link), 'visited': False}
			save_link_to_database(link_object)
		else:
			return
	
	# Make a list of all connections just made
	source = False
	try:
		source = links.objects.filter(Q(destination=url) | Q(description=(url + '/')))[0]
	except:
		pass
	destinations = list(links.objects.filter(source=url))
	
	# Prep lists and generate pageranks
	if source:
		_links = [source] + destinations
		_edges = edges.objects.filter(pointA=source)
	
		pageranks = PR_from_db(_edges, _links, len(_links))
		#print(pageranks)
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
