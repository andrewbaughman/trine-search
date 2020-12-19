import requests
from bs4 import BeautifulSoup

all_links = []

def get_page(url):
	print("Now entering " + url)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.findAll('a')
	for link in links:
		if link.get('href') == None:
			continue
		else:
			if link.get('href')[0:8] == 'http://' or link.get('href')[0:8] == 'https://':
				if link.get('href') in all_links:
					continue
				else:
					all_links.append(link.get('href'))

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


all_links.append('https://en.wikipedia.org/wiki/Main_Page')
for link in all_links:
	print(str(len(all_links)) + " links total")
	print('X' * 500)
	get_page(link)
	parsed_page = get_page_info(link)
	#save_page_to_database(parsed_page)