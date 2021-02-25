from engine.models import Index, Document
from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm
import pickle, multiprocessing

global tokenIndex
#pbar = tqdm(total=3488951)

with open("frequency_index.pkl", 'rb') as f:
    frequency_index = pickle.load(f)

not_rare_words = tuple(key for key, value in frequency_index.items() if value > 2)

tokenIndex = {token: token_id for token_id, token in enumerate(not_rare_words)}

# tokenIndex['___'] = len(not_rare_words)
# rare = Index(Dict = dict())
# rare.id = tokenIndex['___']

print("init...")
Index.objects.all().delete()
objs = []
for i in tqdm(range(len(not_rare_words))):
    objs.append(Index(pk=tokenIndex[not_rare_words[i]]))
    if i % 19999 == 0:
        Index.objects.bulk_create(objs)
        del objs
        objs = []
Index.objects.bulk_create(objs)
del objs

with open("token_index.pkl", 'wb') as f:
    pickle.dump(tokenIndex, f)

Document.objects.all().delete()

objs = []

print("working...")
with open("docs.txt", "r") as f:
    for count in tqdm(range(3040000)):
        content = f.readline()[:-1]
        if count < 1080000:
            del content
            continue
        if content:
            doc_id, tokens = content.split("\t")
            tinyIndex = dict()
            for idx, token in enumerate(tokens.split()):
                try:
                    tinyIndex[token].append(idx)
                except KeyError:
                    tinyIndex[token] = [idx]
            for token, indexes in tinyIndex.items():
                objs.append(Document(
                    token_id = tokenIndex[token],
                    api_id = int(doc_id),
                    List = indexes))
            del doc_id, content, tokens, tinyIndex, idx, token, indexes
            if count % 9999 == 0:
                Document.objects.bulk_create(objs)
                del objs
                objs = []
        else:
            Document.objects.bulk_create(objs)
            del objs
            break
