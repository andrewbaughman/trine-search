import requests
from bs4 import BeautifulSoup
import json
from keywords import *


def is_duplicate_page(url):
	host = 'http://127.0.0.1:8000/add_page/'
	parsed_page = {}
	parsed_page['url'] = url
	parsed_page['method'] = 'is_duplicate_page'
	r = requests.post(url=host, data=parsed_page)
	return r.json()['is_duplicate_page']

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


def save_keywords_to_database(url, keywords):
	host = 'http://127.0.0.1:8000/add_link/'
	parsed_page = {}
	parsed_page['url'] = url
	parsed_page['keywords'] = json.dumps(keywords)
	parsed_page['method'] = 'add_keywords'
	r = requests.post(url=host, data=parsed_page)
	print("Post successful")

def save_page_to_database(parsed_page):
	host = 'http://127.0.0.1:8000/add_page/'
	parsed_page['method'] = 'add_page'
	r = requests.post(url=host, data=parsed_page)
	print("Post successful")
	
x = input("How many links do you want to parse?: ")
host = 'http://127.0.0.1:8000/add_page/'
i = 3
while i <= int(x):
	r = requests.post(url='http://127.0.0.1:8000/add_link/', data={'id': i, 'method': 'get_link'})
	link = r.json()['links']['destination']
	if is_duplicate_page(link):
		print("" + link + " is a duplicate page. Skipping...")
		x = int(x) + 1
	else:
		print("now entering: " + link)
		parsed_page = get_page_info(link)
		keywords = get_word_frequency(link)
		save_keywords_to_database(link, keywords)

		if parsed_page:
			save_page_to_database(parsed_page)
	i = r.json()['links']['id'] + 1
	print(i)


