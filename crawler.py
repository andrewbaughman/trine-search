import requests
from bs4 import BeautifulSoup
import json

inclusion = {"trine", "Trine"}

def trine_url(url):
	for i in inclusion:
		if i in url:
			return True
	return False

def is_duplicate_link(link):
	host = 'http://127.0.0.1:8000/add_link/'
	link_object = {}
	link_object['destination'] = link
	link_object['method'] = 'is_duplicate_link'
	r = requests.post(url=host, data=link_object)
	return r.json()['is_duplicate_link']

def get_page(url):
	print("Now entering " + url)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.findAll('a')
	for link in links:
		href = link.get('href')
		if href == None:
			continue
		else:
			if href[0:7] == 'http://' or href[0:8] == 'https://':
				host = 'http://127.0.0.1:8000/add_page/'
				parsed_page = get_page_info(href)
				if (parsed_page):
					save_page_to_database(parsed_page)
			# search for subpage of url that meets the criteria
			elif (href[0] == '/'):
				host = 'http://127.0.0.1:8000/add_page/'
				parsed_page = get_page_info(url + href[1:])
				if (parsed_page):
					save_page_to_database(parsed_page)
					

def get_page_info(url):
	parsed_page = {}
	
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	if soup.find('title'):
		title = soup.find('title').get_text()
		parsed_page['title'] = title
	else:
		return False

	if soup.find('p'):
		description = soup.find('p').get_text()
		parsed_page['description'] = description

	parsed_page['url'] = url
	
	return parsed_page


def save_page_to_database(parsed_page):
	host = 'http://127.0.0.1:8000/add_page/'
	# check for duplicate before sending
	if is_duplicate_link(parsed_page['url']) == False:
		parsed_page['method'] = 'add_page'
		r = requests.post(url=host, data=parsed_page)
		print("Post successful")

def save_link_to_database(link_object):
	host = 'http://127.0.0.1:8000/add_link/'
	# check for duplicate before sending
	if is_duplicate_link(link_object['destination']) == False:
		link_object['method'] = 'add_link'
		r = requests.post(url=host, data=link_object)
		print("Link post successful")
		input("Happy?")

# get inputs from user
link = ""
while not (link[0:7] == 'http://' or link[0:8] == 'https://'):
	link = input("provide seed link:")
	if not link[0] == 'h':
		print("NOTE: provide in http:// or https:// form")

x = input("provide an integer for the number of iterations:")
int(x)

link_object = {'destination': link, 'source': "", 'isTrine': trine_url(link), 'visited': False, 'method': 'add_link'}
save_link_to_database(link_object)

i = 0
while i < 3:
	host = 'http://127.0.0.1:8000/add_page/'
	r = requests.post(url=host, data={'id': i, 'method': 'get_link'})
	link = r.json()['page_results']['url']
	get_page(link)
	i = r.json()['page_results']['id'] + 1
	print(i)

