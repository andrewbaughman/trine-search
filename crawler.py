import requests
from bs4 import BeautifulSoup
import json

def is_duplicate_link(url):
	host = 'http://127.0.0.1:8001/add_page/'
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
			if href[0:8] == 'http://' or href[0:8] == 'https://':
				print("Is duplicate: " + str(is_duplicate_link(href)))
				# Check to see if the link already exists
				if is_duplicate_link(href):
					continue
				else:
					host = 'http://127.0.0.1:8001/add_page/'
					parsed_page = {'url': href, 'title': "", 'description': "", 'method': 'add_page'}
					r = requests.post(url=host, data=parsed_page)
					

def get_page_info(url):
	parsed_page = {}
	
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	title = soup.find('title').get_text()
	description = soup.find('p').get_text()

	print("Title: " + title)
	print("Description: " + description)
	#print(soup)

	parsed_page['url'] = url
	parsed_page['title'] = title
	parsed_page['description'] = description

	return parsed_page


def save_page_to_database(parsed_page):
	host = 'http://127.0.0.1:8001/add_page/'
	parsed_page['method'] = 'add_page'
	r = requests.post(url=host, data=parsed_page)
	if r.json()['page']['url'] == parsed_page['url']:
		print("Post successful")
	
i = 0
while i < 20:
	host = 'http://127.0.0.1:8001/add_page/'
	r = requests.post(url=host, data={'id': i, 'method': 'get_link'})
	link = r.json()['page']['url']
	get_page(link)
	parsed_page = get_page_info(link)
	save_page_to_database(parsed_page)
	parsed_page = get_page_info(link)
	save_page_to_database(parsed_page)
	i = r.json()['page']['id'] + 1
	print(i)
