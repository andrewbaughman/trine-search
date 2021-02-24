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

#Controls how many words are returned
num_results = 20
#Print intermediate? 1=Yes,else=No
deb = 0
#List of stop words found at http://xpo6.com/list-of-english-stop-words/
exception_list = ("a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the")

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
        for z in exception_list:
            if (i==z):
                if (deb==1):
                    print("Blocked word: " + z)
                exception_flag = 1
                break
        if (exception_flag == 0):
            final_list[i] = word_list.count(i)
            if (deb==1):
                print("Loaded word: " + i)
        exception_flag = 0
    #Sort by count found at https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    final_list = dict(sorted(final_list.items(), key=lambda item: item[1], reverse=True))
    #Print the full list
    if (deb==1):
        print(final_list)
    #for loop to print first "num_results" results in dict .items() fix found at https://careerkarma.com/blog/python-valueerror-too-many-values-to-unpack-expected-2/#:~:text=Conclusion,to%20iterate%20over%20a%20dictionary.
    break_condition = 0
    return_list = {}
    for key, value in final_list.items():
        if (deb==1):
            print(key, ": ", value)
        return_list[key] = value
        break_condition = break_condition + 1
        if(break_condition == num_results):
            break
    return return_list


def get_metadata_info(soup):
    #List declarations
    final_list = []
    metataginfo_list = []
    metatag_list = []
    header_list = []
    title_list = []
    #for loops for finding important tags from http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
    metataginfo_tags = soup.find_all('head')
    for i in range(len(metataginfo_tags)):
        element_found = ((re.sub(r'[^\w\s]', '', soup.find_all('head')[i].text)).lower()).split()
        metataginfo_list.extend(element_found)
        if (deb == 1):
            print("Found and loaded: " + str(element_found))
    if (deb == 1):
        print("All metatag info found: " + str(metataginfo_list))
    
    metatag_tags = soup.find_all('meta')
    for i in range(len(metatag_tags)):
        element_found = ((re.sub(r'[^\w\s]', '', soup.find_all('meta')[i].text)).lower()).split()
        metatag_list.extend(element_found)
        if (deb == 1):
            print("Found and loaded: " + str(element_found))
    if (deb == 1):
        print("All meta info found: " + str(metatag_list))
    
    header_tags = soup.find_all('header')
    for i in range(len(header_tags)):
        element_found = ((re.sub(r'[^\w\s]', '', soup.find_all('header')[i].text)).lower()).split()
        header_list.extend(element_found)
        if (deb == 1):
            print("Found and loaded: " + str(element_found))
    if (deb == 1):
        print("All header info found: " + str(header_list))
    
    title_tags = soup.find_all('title')
    for i in range(len(title_tags)):
        element_found = ((re.sub(r'[^\w\s]', '', soup.find_all('title')[i].text)).lower()).split()
        title_list.extend(element_found)
        if (deb == 1):
            print("Found and loaded: " + str(element_found))
    if (deb == 1):
        print("All title info found: " + str(title_list))        

    final_list.extend(metataginfo_list)
    final_list.extend(metatag_list)
    final_list.extend(header_list)
    final_list.extend(title_list)

    final_list = set(final_list)

    return_list = []
    exception_flag = 0
    #for loop to load/discard words
    for i in final_list:
        for z in exception_list:
            if (i==z):
                if (deb==1):
                    print("Blocked word: " + z)
                exception_flag = 1
                break
        if (exception_flag == 0):
            return_list.append(i)
            if (deb==1):
                print("Loaded word: " + i)
        exception_flag = 0

    return return_list

def get_keywords(soup):
    keywords = {}
    keywords_meta = {}
    keywords_frequency = {}
    frequency_words = get_word_frequency(soup)
    metadata_words = get_metadata_info(soup)
    #Load frequency_words into dict
    for key, value in frequency_words.items():
        keywords_meta[key] = value
    #Load metadata_words into dict
    for i in metadata_words:
        #Make metadata_words have weight, like frequency_words have by giving them weight one above that of the first value in frequency_words
        #First key finder code found at https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
        keywords_frequency[i] = 1 + frequency_words[next(iter(frequency_words))]
    #Add the two dicts together
    #Code from https://stackoverflow.com/questions/6005066/adding-dictionaries-together-python
    keywords = dict(keywords_frequency, **keywords_meta)
    #Adjust for words that are in both dicts, adding their values together
    for key in keywords_meta:
        if key in keywords_frequency:
            keywords[key] = keywords_meta[key] + keywords_frequency[key]
    #Sort by value
    keywords = dict(sorted(keywords.items(), key=lambda item: item[1], reverse=True))

    return keywords