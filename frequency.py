#The get_word_frequency function returns a dict of "num_results"-size, where the value is equal to
#the number of times its key is mentioned on the corresponding webpage to the provided url.
import requests
from bs4 import BeautifulSoup
import json
import re

#Controls how many words are returned
num_results = 20
#Print intermediate? 1=Yes,else=No
deb = 0

def get_word_frequency(url):
    if (deb==1):
        print("Now fetching word frequency data from: " + url)
    #Set up soup object with string of webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')        
    #Remove punctuation from string found at https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
    text_no_punct = re.sub(r'[^\w\s]', '', soup.get_text()) 
    #Lowercase string
    text_lowercase = text_no_punct.lower()
    #Break at spaces and put into list
    word_list = text_lowercase.split()
    #Put into set so duplicate values are removed
    unique_word_list = list(set(word_list))
    #List of stop words found at http://xpo6.com/list-of-english-stop-words/
    exception_list = ("a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the")
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

