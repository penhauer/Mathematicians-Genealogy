import re
import string
import sys
import urllib.request

from nltk.stem.porter import PorterStemmer
from tqdm import tqdm
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords

regex = re.compile(r'[^a-z\s]')
punctuation = re.compile('[' + string.punctuation + ']')
porter = PorterStemmer()

prep = input('Should I preprocess? y/n')
prep = prep == 'y'

for line in sys.stdin:
    current_url = line.strip().split(';')[2].strip()
    url = urllib.request.urlopen(current_url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')

    name = soup.main.div.text.strip().replace(' ', '_')

    if name:
        if prep:
            text = soup.main.get_text().lower()
            text = re.sub(punctuation, ' ', text)
            text = re.sub(regex, '', text)
            words = word_tokenize(text)
            words = [word for word in words if len(word) > 1]
            stop_words = stopwords.words('english')
            words = [word for word in words if word not in stop_words]
            stems = [porter.stem(word) for word in words]

        print(name)
        file = open(f'texts/{name}', 'w+')
        file.write(' '.join(stems))
        file.close()
        print()
