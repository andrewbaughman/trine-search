import requests
from bs4 import BeautifulSoup
import json
import time
import signal

inclusion = {"trine", "Trine"}

#https://code-maven.com/python-timeout
class TimeOutException(Exception):
   pass

def alarm_handler(signum, frame):
    print("timeout has occured")
    raise TimeOutException()

# from https://www.geeksforgeeks.org/python-ways-to-find-nth-occurrence-of-substring-in-a-string/
def loc_third_slash(link):
	occurrence = 3
	inilist = [i for i in range(0, len(link)) 
            if link[i:].startswith('/')] 
	if len(inilist)>= 3:
		return inilist[occurrence-1]
	else: 
		return False

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

def get_page_of_links(url):
	signal.signal(signal.SIGALRM, alarm_handler)
	signal.alarm(10)
	print("Now entering " + url)
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		links = soup.findAll('a')
	except TimeOutException as ex:
		print(ex)
	except:
		print("error in soup")
	signal.alarm(0)
	for link in links:
		href = link.get('href')
		if href == None:
			continue
		elif href:
			if href[0:7] == 'http://' or href[0:8] == 'https://':
				host = 'http://127.0.0.1:8000/add_link/'
				link_object = {'destination': href, 'source': url, 'isTrine': trine_url(href), 'visited': False, 'method': 'add_link'}
				save_link_to_database(link_object)
			# search for subpage of url that meets the criteria
			elif (href[0] == '/'):
				host = 'http://127.0.0.1:8000/add_link/'
				if(loc_third_slash(url)):
					url =  url[0:loc_third_slash(url)]
				appended_link = url + href
				link_object = {'destination': appended_link, 'source': url, 'isTrine': trine_url(appended_link), 'visited': False, 'method': 'add_link'}
				save_link_to_database(link_object)
					
def save_link_to_database(link_object):
	host = 'http://127.0.0.1:8000/add_link/'
	# check for duplicate before sending
	if is_duplicate_link(link_object['destination']) == False:
		link_object['method'] = 'add_link'
		r = requests.post(url=host, data=link_object)
		print("Link post successful")

if __name__ == '__main__':
	# get inputs from user
	link = ""
	while not (link[0:7] == 'http://' or link[0:8] == 'https://'):
		link = input("provide seed link:")
		if not link[0] == 'h':
			print("NOTE: provide in http:// or https:// form")

	if (not (is_duplicate_link(link))):
		link_object = {'destination': link, 'source': "", 'isTrine': trine_url(link), 'visited': False, 'method': 'add_link'}
		save_link_to_database(link_object)

	i = 0
	while 1:
		host = 'http://127.0.0.1:8000/add_link/'
		r = requests.post(url=host, data={'id': i, 'method': 'get_link'})
		link = r.json()['links']['destination']
		try:
			get_page_of_links(link)
		except:
			print("undefined error in get_page_of_links")
		i = r.json()['links']['id'] + 1
		print(i)

