from engine.models import Index
from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm
import pickle

global tokenIndex
tokenIndex = dict()
new_id = 1
pbar = tqdm(total=3488951)
Index.objects.all().delete()

with open("frequency_index.pkl", 'rb') as f:
    # already take out words with freq == 1
    frequency_index = pickle.load(f)
not_rare_words = tuple(frequency_index.keys())

def token2id(token, new_id):
    if token not in not_rare_words:
            token = '___'
    if token in tokenIndex:
        return tokenIndex[token], new_id
    else:
        tokenIndex[token] = new_id
        return tokenIndex[token], new_id + 1

with open("docs.txt", "r") as f:
    while True:
        content = f.readline()[:-1]
        if content:
            doc_id, tokens = content.split("\t")
            # loop over tokenized document
            for idx, token in enumerate(tokens.split()):
                # get id of the token
                token_id, new_id = token2id(token, new_id)
                try:
                    temp = Index.objects.get(pk=token_id)
                    if doc_id not in temp.Dict:
                        temp.Dict[doc_id] = [idx]
                    else:
                        temp.Dict[doc_id].append(idx)
                except ObjectDoesNotExist:
                    temp = Index(Dict = {doc_id: [idx]})
                    temp.id = token_id
                temp.save()
            del doc_id, content, tokens, token_id, temp
            pbar.update(1)
        else:
            pbar.close()
            break

with open("token_index.pkl", 'wb') as f:
    pickle.dump(tokenIndex, f)
