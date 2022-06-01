import re
import string
import glob

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity

regex = re.compile(r'[^a-z\s]')
punctuation = re.compile('[' + string.punctuation + ']')
porter = PorterStemmer()
stop_words = stopwords.words('english')

filenames = [filename for filename in glob.glob('short/*')]

files = []
for f in filenames:
    f = open(f, 'r')
    files.append(f.read())
    f.close()

vectorizer = TfidfVectorizer(strip_accents='unicode', stop_words='english')
matrix = vectorizer.fit_transform(files)

k = 10

filenames = [filename[6:] for filename in filenames]

query = input('What are you looking for? ')
while query != 'exit':
    query = query.lower()
    query = re.sub(punctuation, ' ', query)
    query = re.sub(regex, '', query)
    query = word_tokenize(query)
    query = [word for word in query if len(word) > 1]
    query = [word for word in query if word not in stop_words]
    query = [porter.stem(word) for word in query]
    query = ' '.join(query)
    query_vec = vectorizer.transform([query])
    results = reversed(cosine_similarity(matrix, query_vec).reshape((-1)).argsort()[-k:])
    for i in results:
        print(filenames[i].replace('_', ' '))
    query = input('What are you looking for? ')
