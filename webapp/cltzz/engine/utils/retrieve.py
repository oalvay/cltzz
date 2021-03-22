import numpy as np
from ..models import Song
import scipy.sparse
from pickle import load as pload
import re, string
from time import time as ttime
from sklearn.feature_extraction.text import TfidfVectorizer as ngram
from sentence_transformers import SentenceTransformer, util
from scipy.sparse.linalg import norm
from copy import deepcopy

ST = SentenceTransformer('paraphrase-distilroberta-base-v1')

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

def clean_title(text: str)-> str:
    text = re.sub("\([^\(\)]+\)", "", text)
    text = re.sub('\s+', ' ', text)
    return text.lower()

clean = lambda text: " ".join(tokenize(text))

def retrieve(query: str, docs_num: int)-> list:
    """basic ranked retrieve using TFIDF
    docs_num: number of documents to retrieve"""
    terms = tuple([token_index[token] for token in tokenize(query) if token in token_index])

    if len(terms) <= 0 or len(terms) >= 30:
        return [], clean(query)
    
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
    
    rank = np.argsort(tfidf)[::-1][:docs_num]
    
    return rank, clean(query)

def rerank(retrieved:list, query:str, bert = False)-> list:
    """rerank retrieved documents with complex models (n-gram etc)"""
    lyricses = tuple(clean(Song.objects.get(pk=doc_id).lyrics) for
                     doc_id in retrieved)

    abstracts = tuple(" ".join(lyrics.split()[:50]) for lyrics in lyricses)

    model = ngram(ngram_range=(1,5))
    model.fit([query])
    
    result = model.transform(lyricses).sum(axis=1).A

    # normer = deepcopy(result)
    # normer.data *= normer.data
    # print(normer)

    if bert:    
        lyricses_embeddings = ST.encode(abstracts)
        query_embedding = ST.encode(query)

        cosine_scores = util.pytorch_cos_sim(query_embedding,
                                             lyricses_embeddings).numpy().reshape(-1,1)
        
        result += (cosine_scores - cosine_scores.min())/\
                    (cosine_scores.max() - cosine_scores.min())
    
    
    return [x for _,x in sorted(zip(result,retrieved), reverse = True)]


