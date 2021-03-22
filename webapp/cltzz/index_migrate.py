from tqdm import tqdm
import pickle
from scipy.sparse import dok_matrix, csc_matrix, save_npz
import numpy as np
from collections import Counter

with open("docs_id.pkl", 'rb') as f:
    docs_id = pickle.load(f)
    
docs_id = {docs_id:idx for idx, docs_id in enumerate(docs_id)}
    
doc_len = len(docs_id)

with open("token_index.pkl", 'rb') as f:
    token_index = pickle.load(f)
    
token_index = {key:ids for ids, key in enumerate(token_index.keys())}

freq_matrix = dok_matrix((doc_len, len(token_index)+1), dtype=np.uint8)

with open("docs.txt", "r") as f:
    for count in tqdm(range(doc_len)):
        content = f.readline()[:-1]
        if content:
            rl_doc_id, tokens = content.split("\t")
            tokens = Counter(tokens.split())
            doc_id = docs_id[int(rl_doc_id)]
            for token, freq in tokens.items():
                freq_matrix[doc_id, token_index[token]] = freq if freq < 255 else 255
            del doc_id, tokens, content, freq, token
            
save_npz("freq_matrix.npz", csc_matrix(freq_matrix))

with open("token_reindex.pkl", 'wb') as f:
    pickle.dump(token_index, f)