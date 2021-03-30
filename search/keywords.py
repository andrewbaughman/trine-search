#The get_word_frequency function returns a dict of "num_results"-size, where the value is equal to
#the number of times its key is mentioned on the corresponding webpage to the provided url.

#The get_metadata_info function returns a list of words that are significant for a webpage, based
#on their HTML tags.

#The get_keywords function returns a dict of the keywords found using the get_word_frequency function
#and the get_metadata_info function

import requests
from bs4 import BeautifulSoup
import json
import re

#Controls how many words are returned for get_word_frequency and get_keywords
num_results = 100
sum_adj = num_results**2
#List of stop words found at http://xpo6.com/list-of-english-stop-words/
exception_list = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the")

def get_word_frequency(soup):
    #Remove punctuation from string found at https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
    text_no_punct = re.sub(r'[^\w\s]', '', soup.get_text()) 
    #Lowercase string
    text_lowercase = text_no_punct.lower()
    #Break at spaces and put into list
    word_list = text_lowercase.split()
    #Put into set so duplicate values are removed
    unique_word_list = list(set(word_list))
    
    final_list = {}
    exception_flag = 0
    #for loop to load/discard words
    for i in unique_word_list:
        if i not in exception_list and len(i) <= 20:
            final_list[i] = word_list.count(i)
    
    #Sort by count found at https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    final_list = dict(sorted(final_list.items(), key=lambda item: item[1], reverse=True)[:num_results])
    
    #.items() fix found at https://careerkarma.com/blog/python-valueerror-too-many-values-to-unpack-expected-2/#:~:text=Conclusion,to%20iterate%20over%20a%20dictionary.
    #Don't know if ^ link is referenced elsewhere

    return final_list


def get_metadata_info(soup):
    #List declarations
    final_list = []
    metataginfo_list = []
    metatag_list = []
    title_list = []
    
    #for loops for finding important tags from http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
    metataginfo_tags = soup.find_all('head')
    for i in range(len(metataginfo_tags)):
        element_found = ((re.sub(r'[^\w\s]', '', soup.find_all('head')[i].text)).lower()).split()
        metataginfo_list.extend(element_found)
    
    metatag_tags = soup.find_all('meta')
    for i in range(len(metatag_tags)):
        #.get fix found at https://realpython.com/python-keyerror/#:~:text=The%20Python%20KeyError%20is%20a,for%20could%20not%20be%20found.
        if(metatag_tags[i].attrs.get('name') == ('Keywords' or 'keywords')):
            element_found = ((re.sub(r'[^\w\s]', '', metatag_tags[i].attrs['content'])).lower()).split()
            metatag_list.extend(element_found)
        element_found = ((re.sub(r'[^\w\s]', '', soup.find_all('meta')[i].text)).lower()).split()
        metatag_list.extend(element_found)
    
    title_tags = soup.find_all('title')
    element_found = ((re.sub(r'[^\w\s]', '', title_tags[0].text)).lower()).split()
    element_list = list()
    for element in element_found:
        element_ms = element
        if element[-1] == 's':
            element_ms = element_ms[:(len(element_ms) -1)]
        if ((element + 's') not in element_list) & (element_ms not in element_list):
            element_list.append(element)    
    title_list.extend(element_list) 
    
    final_list.extend(metataginfo_list)
    final_list.extend(metatag_list)
    final_list.extend(title_list)

    final_list = set(final_list)
    return_list = []
    #for loop to load/discard words
    for i in final_list:
        if i not in exception_list and len(i) <= 20:
            return_list.append(i)

    return return_list

def get_keywords(soup):
    keywords = {}
    keywords_intermed = {}
    keywords_meta = {}
    keywords_frequency = get_word_frequency(soup)
    metadata_words = get_metadata_info(soup)
    
    #Load metadata_words into dict
    for i in metadata_words:
        #Make metadata_words have a value, like frequency_words have by giving them a value one above that of the first value in frequency_words
        #First key finder code found at https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
        keywords_meta[i] = 1 + keywords_frequency[next(iter(keywords_frequency))]
    
    #Add the two dicts together
    #Code from https://stackoverflow.com/questions/6005066/adding-dictionaries-together-python
    keywords = dict(keywords_frequency, **keywords_meta)
    
    #Adjust for words that are in both dicts, adding their values together
    for key in keywords_meta:
        if key in keywords_frequency:
            keywords[key] = keywords_meta[key] + keywords_frequency[key]

    #Adjust value in regard to the sum of values in dict
    total = sum(keywords.values())
    lowest_value = num_results*min(keywords.values())
    if lowest_value > total:
        total = lowest_value
    for key, value in keywords.items():
        tempsum = (value*sum_adj) / total
        if tempsum <= 1:
            keywords_intermed[key] = 1
        else:
            keywords_intermed[key] = int(round(tempsum))
    
    #Sort by value
    keywords_intermed = dict(sorted(keywords_intermed.items(), key=lambda item: item[1], reverse=True)[:num_results])
        
    return keywords_intermed