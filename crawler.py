import requests
from bs4 import BeautifulSoup
import json

def is_duplicate_link(url):
	host = 'http://127.0.0.1:8000/add_page/'
	url_dict = {}
	url_dict['url'] = url
	url_dict['method'] = 'is_duplicate'
	r = requests.post(url=host, data=url_dict)
	return r.json()['is_duplicate']

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
				# ensure that page is useful
				if ("trine" in href):
					host = 'http://127.0.0.1:8000/add_page/'
					parsed_page = get_page_info(href)
					save_page_to_database(parsed_page)
			# search for subpage of url that meets the criteria
			elif href[0] == '/' and "trine" in url:
				if ("trine" in url):
					host = 'http://127.0.0.1:8000/add_page/'
					parsed_page = get_page_info(url + href[0:])
					save_page_to_database(parsed_page)
					

def get_page_info(url):
	parsed_page = {}
	
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	if soup.find('title'):
		title = soup.find('title').get_text()
		parsed_page['title'] = title

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
	
i = 0
while i < 3:
	host = 'http://127.0.0.1:8000/add_page/'
	r = requests.post(url=host, data={'id': i, 'method': 'get_link'})
	link = r.json()['page']['url']
	get_page(link)
	parsed_page = get_page_info(link)
	i = r.json()['page']['id'] + 1
	print(i)

