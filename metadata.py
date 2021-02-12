import requests
from bs4 import BeautifulSoup
import json
import re

def get_metadata_info(url):
    print("Now fetching metatag data from: " + url)
    #Set up soup object with string of webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #List declarations
    final_list = [] 
    word_list = []
    metataginfo_list = []
    metatag_list = []
    header_list = []
    title_list = []

    a

    
    #for loops for finding important tags from http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
    #range(len(metataginfo_tags))
    metataginfo_tags = soup.find_all('head')
    for i in metataginfo_tags:
        print("Found: " + str(i.data))
        metataginfo_list.extend(((re.sub(r'[^\w\s]', '', soup.find('head')[i].text)).lower()).split())
    print(metataginfo_list)


    #final_list = list(set(word_list))

