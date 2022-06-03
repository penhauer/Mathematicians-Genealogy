import re
import string
import glob

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity

nonstandard = re.compile(r'[^a-z\s]')
punctuation = re.compile('[' + string.punctuation + ']')
stop_words = stopwords.words('english')
stemmer = PorterStemmer()


def preprocess(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(punctuation, ' ', text)
    text = re.sub(nonstandard, '', text)
    text = word_tokenize(text)
    text = [token for token in text if len(token) > 1]
    text = [token for token in text if token not in stop_words]
    text = [stemmer.stem(token) for token in text]
    return text


filenames = [filename for filename in glob.glob('short/*')]

files = []
for filename in filenames:
    file = open(filename, 'r')
    files.append(file.read())
    file.close()

vectorizer = TfidfVectorizer(strip_accents='unicode', stop_words='english')
matrix = vectorizer.fit_transform(files)

k = 10

filenames = [filename[6:] for filename in filenames]

query = input('What are you looking for? ')
while query != 'exit':
    query = preprocess(query)
    query = ' '.join(query)
    query = vectorizer.transform([query])

    results = reversed(cosine_similarity(matrix, query).reshape((-1)).argsort()[-k:])
    for i in results:
        print(filenames[i].replace('_', ' '))
    query = input('What are you looking for? ')
