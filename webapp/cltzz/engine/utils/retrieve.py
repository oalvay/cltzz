import numpy as np
from ..models import Song
import re, string

def tokenize(text):
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'(www|http)\S+', '', text.lower())
    text = re.sub("\[.*\]", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', string.digits))
    return text.split()

def weight(term, document):
    try:
        termFreq = len(indexList[term][document])
        docFreq = len(indexList[term])
        return (1 + np.log10(termFreq)) * np.log10(len(ids_list)/docFreq)
    except KeyError:
        docFreq = len(indexList[term])
        return np.log10(len(ids_list)/docFreq)
    
HAS = lambda word: set(indexList[word].keys())
    
def search(query):
    terms = tokenize(query)
    matchDoc = set.union(*map(HAS, terms))
    
    scores = [[document, list(weight(term, document) for term in terms)]
        for document in matchDoc]
    return sorted(scores, key=lambda x: x[1], reverse = True)