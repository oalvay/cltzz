# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 20:30:29 2021

@author: siyue chen, zhendong tian, zhuocheng zheng.
"""

import pandas as pd
import string
import re
from nltk.tokenize import word_tokenize
import numpy as np
from tqdm import tqdm
from collections import Counter

import pickle
def isEnglish(s):
    return sum([ord(i)<128 for i in s]) / len(s) > 0.99 and len(s) > 5

class Processor:
    
    def __tokenize(self, text):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'www\S+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.translate(str.maketrans('', '', string.digits))
        stringlist = text.split()
        return stringlist
    
    def __init__(self):
        datafile = 'data_1_1000000.csv'
        self.data = pd.read_csv(
        datafile, sep = "\t", error_bad_lines=False, warn_bad_lines=False, na_values = "_",
        )
        self.data.lyrics = self.data.lyrics.astype('str')
        
        self.id_lyrics_dic = {}
        for i in range(len(self.data)):
            item =self.data.iloc[i]
            api_id = item['api_id']
            lyric = item['lyrics']
            if(isEnglish(lyric)):
                self.id_lyrics_dic[api_id] = lyric
        
        self.id_lyrics_dic.pop(290125)
        
        self.lyrics_list = list(self.id_lyrics_dic.values())
        
        self.docs = [i.casefold() for i in self.lyrics_list]
        
        self.tokenized_docs = [self.__tokenize(i) for i in self.docs]
        self.doc_dict = {i:list_ for i, list_ in zip(self.data.api_id.to_list(), self.tokenized_docs)}
        with open("doc_ids.obj",'wb') as f:
            pickle.dump(self.data.api_id.to_list(),f)
        text = "\n".join(self.docs)
        
        self.term_dict = {}
        for d_id,doc in tqdm(self.doc_dict.items()):
            for index,t in enumerate(doc):
                if t not in self.term_dict:
                    self.term_dict[t] = {}
                    self.term_dict[t][d_id] = [index]
                elif d_id not in self.term_dict[t]:
                    self.term_dict[t][d_id] = [index]
                    
                else:
                    self.term_dict[t][d_id].append(index)
                    
        #Saved as pickle
        with open("term_dict.obj",'wb') as f:
            pickle.dump(self.term_dict,f)
        
        #Build inverted lists
        self.inv_lists = self.doc_vector.T
        
        #Build incidence matrix
        self.incidence_matrix = self.inv_lists != 0
        
        #Build Sparse inverted Lists
        self.prepare_sparse_inverted_list()
        
        #Build Positional Index
        self.build_positional_index()
        
    def get_doc_vector_matrix(self):
        return self.doc_vector
    
    def get_incidence_matrix(self):
        return self.incidence_matrix
    
    def prepare_sparse_inverted_list(self):
        flat_im = np.where(self.get_incidence_matrix().flatten())
        recurrent_doc_index = flat_im[0] % len(self.docs) + 1
        empty_flatten_matrix = np.zeros((len(self.tokens),len(self.docs))).flatten()
        empty_flatten_matrix[flat_im] = recurrent_doc_index
        inverted_index_matrix = empty_flatten_matrix.reshape(len(self.tokens),len(self.docs))
        inverted_index = [[int(i-1) for i in l if i!=0]for l in inverted_index_matrix]
        sparse_inverted_list = [[(j,self.inv_lists[i][j]) for j in inverted_index[i]] for i in range(len(self.tokens))]
        self.sparse_inverted_list = sparse_inverted_list
        return self.sparse_inverted_list

    def build_positional_index(self):
        self.positional_index = {i : {j : np.where(np.array(self.tokenized_docs[j]) == self.tokens[i])[0].tolist() for (j,_) in self.sparse_inverted_list[i]} for i in range(len(self.sparse_inverted_list))}
