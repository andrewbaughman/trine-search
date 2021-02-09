import requests
from bs4 import BeautifulSoup
import json

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
	parsed_page['method'] = 'add_page'
	r = requests.post(url=host, data=parsed_page)
	print("Post successful")
	
x = input("How many links do you want to parse?: ")
host = 'http://127.0.0.1:8000/add_page/'
i = 0
while i < int(x):
    r = requests.post(url='http://127.0.0.1:8000/add_link/', data={'id': i, 'method': 'get_link'})
    link = r.json()['links']['destination']
    print("now entering: " + link)
    parsed_page = get_page_info(link)
    if parsed_page:
        save_page_to_database(parsed_page)
    i = r.json()['links']['id'] + 1
    print(i)