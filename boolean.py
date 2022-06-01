import re
import string
import glob

import pandas as pd

from tqdm import tqdm
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords

regex = re.compile(r'[^a-z\s]')
punctuation = re.compile('[' + string.punctuation + ']')
porter = PorterStemmer()

unique_words = set()

for file in glob.glob('short/*'):
    file = open(file, 'r')
    words = set(file.read().split())
    file.close()
    unique_words = unique_words.union(words)

docs = []

for file in glob.glob('short/*'):
    doc = {'DOCUMENT_NAME': file[6:]}
    file = open(file, 'r')
    words = set(file.read().split())
    file.close()

    for word in unique_words:
        if word in words:
            doc[word] = 1
        else:
            doc[word] = 0

    docs.append(doc)
    unique_words = unique_words.union(words)

columns = ['DOCUMENT_NAME'] + list(unique_words)
docs = pd.DataFrame(docs, columns=columns)
stop_words = stopwords.words('english')

k = 10

query = input('What are you looking for? ')
while query != 'exit':
    query = query.lower()
    query = re.sub(punctuation, ' ', query)
    query = re.sub(regex, '', query)
    query = word_tokenize(query)
    query = [word for word in query if len(word) > 1]
    query = [word for word in query if word not in stop_words]
    query = [porter.stem(word) for word in query]

    ans = docs.copy()
    for word in query:
        if len(ans) > 0:
            ans = ans[ans[word] == 1]
    ans = list(ans.head(k)['DOCUMENT_NAME'])
    ans = [word.replace('_', ' ') for word in ans]
    print(*ans, sep='\n')
    query = input('What are you looking for? ')
