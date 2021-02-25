from tqdm import tqdm
import pickle
from scipy.sparse import dok_matrix, csc_matrix
import scipy.sparse
import numpy as np
global tokenIndex
from collections import Counter
#pbar = tqdm(total=3488951)



with open("token_index.pkl", 'rb') as f:
    token_index = pickle.load(f)

freq_matrix = dok_matrix((6450000, len(token_index)+1), dtype=np.int16)

with open("docs.txt", "r") as f:
    for count in tqdm(range(340000)):
        content = f.readline()[:-1]
        if content:
            doc_id, tokens = content.split("\t")
            doc_id, tokens = int(doc_id), Counter(tokens.split())
            for token, freq in tokens.items():
                freq_matrix[doc_id, token_index[token]] = freq
            del doc_id, tokens, content, freq, token

with open("freq_matrix.pkl", 'wb') as f:
    pickle.load(freq_matrix, f)

save_npz(csc_matrix(freq_matrix), "freq_matrix.npz")