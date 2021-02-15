import requests
from bs4 import BeautifulSoup
import json
import time
import signal

#https://code-maven.com/python-timeout
class TimeOutException(Exception):
   pass

def alarm_handler(signum, frame):
    print("timeout has occured")
    raise TimeOutException()

def is_duplicate_page(url):
	host = 'http://127.0.0.1:8000/add_page/'
	parsed_page = {}
	parsed_page['url'] = url
	parsed_page['method'] = 'is_duplicate_page'
	r = requests.post(url=host, data=parsed_page)
	return r.json()['is_duplicate_page']

def get_page_info(url):
	parsed_page = {}
	signal.signal(signal.SIGALRM, alarm_handler)
	signal.alarm(10)
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
	except TimeOutException as ex:
		print(ex)
	except:
		print("error in soup")
	signal.alarm(0)


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
	
host = 'http://127.0.0.1:8000/add_page/'
i = 0
while 1:
	r = requests.post(url='http://127.0.0.1:8000/add_link/', data={'id': i, 'method': 'get_link'})
	link = r.json()['links']['destination']
	if is_duplicate_page(link):
		print("" + link + " is a duplicate page. Skipping...")
	else:
		print("now entering: " + link)
		parsed_page = None
		try:
			parsed_page = get_page_info(link)
		except:
			print("undefined error in get_page_info")
		if parsed_page:
			save_page_to_database(parsed_page)
	i = r.json()['links']['id'] + 1
	print(i)