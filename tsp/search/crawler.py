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
            if link.get('href')[0:8] == 'https://':
                if link.get('href') in all_links:
                    continue
                else:
                    all_links.append(link.get('href'))

all_links.append('https://www.wikipedia.com/en')
for link in all_links:
    print(str(len(all_links)) + " links total")
    get_page(link)