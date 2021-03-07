import numpy as np
from ..models import Song
import scipy.sparse
from pickle import load as pload
import re, string
from time import time as ttime

with open('../../token_index.pkl', 'rb') as f:
    token_index = pload(f)
with open('../../docs_id.pkl', 'rb') as f:
    docs_len = len(pload(f))

freq_matrix = scipy.sparse.load_npz("../../freq_matrix.npz")

def tokenize(text: str)-> list:
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'(www|http)\S+', '', text.lower())
    text = re.sub("\[[^\[\]]+\]", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', string.digits))
    return text.split()

def retrieve(query: str, docs_num: int)-> list:
    """basic ranked retrieve using TFIDF
    docs_num: number of documents to retrieve"""
    start_time = ttime()
    terms = tuple([token_index[token] for token in tokenize(query) if token in token_index])

    if len(terms) == 0:
        return [], start_time - ttime()
    
    # extract only columns of tokens in the query (duplicated tokens(cols) are possible)
    relevant_freqs = freq_matrix[:, terms].tocsr()

    # https://stackoverflow.com/questions/59338537/summarize-non-zero-values-in-a-scipy-matrix-by-axis
    # get document frequency 
    docFreq = relevant_freqs.astype(bool).sum(axis=0).A1

    # # get matched documents
    # matchDoc = relevant_freqs.astype(bool).sum(axis=1).nonzero()[0]

    # calculate TFIDF
    relevant_freqs.data = np.log10(relevant_freqs.data)

    tfidf = (1 + relevant_freqs.astype(float).toarray()) @ np.log10(docs_len/docFreq)

    return np.argsort(tfidf)[:-docs_num:-1], ttime() - start_time

def rerank(retrieved:list)-> list:
    """rerank retrieved documents with complex models (n-gram etc)"""
    pass
    