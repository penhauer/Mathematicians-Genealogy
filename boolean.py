import re
import string
import glob

import pandas as pd

from typing import List
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize

punctuation = re.compile('[' + string.punctuation + ']')
nonstandard = re.compile(r'[^a-z\s]')
stop_words = stopwords.words('english')
stemmer = PorterStemmer()


def preprocess(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(punctuation, ' ', text)
    text = re.sub(nonstandard, '', text)
    text = word_tokenize(text)
    text = [token for token in text if len(token) > 1]
    text = [token for token in text if token not in stop_words]
    text = [stemmer.stem(token) for token in text]
    return text


unique_words = set()

for filename in glob.glob('short/*'):
    file = open(filename, 'r')
    words = set(file.read().split())
    file.close()
    unique_words = unique_words.union(words)

docs = []

for filename in glob.glob('short/*'):
    doc = {'DOCUMENT_NAME': filename[6:]}
    file = open(filename, 'r')
    words = set(file.read().split())
    file.close()

    for word in unique_words:
        if word in words:
            doc[word] = 1
        else:
            doc[word] = 0

    docs.append(doc)

columns = ['DOCUMENT_NAME'] + list(unique_words)
docs = pd.DataFrame(docs, columns=columns)

k = 10

query = input('What are you looking for? ')
while query != 'exit':
    query = preprocess(query)

    ans = docs.copy()

    for word in query:
        if len(ans) > 0:
            ans = ans[ans[word] == 1]

    ans = list(ans.head(k)['DOCUMENT_NAME'])
    ans = [word.replace('_', ' ') for word in ans]
    print(*ans, sep='\n')
    query = input('What are you looking for? ')
