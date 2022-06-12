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

prep = False
if len(sys.argv) > 1:
    prep = sys.argv[1] == 'y'
print(prep)

ids_dict = {}
with open('ids.txt', 'r') as f:
    for line in f:
        person = line.strip().split('\t')
        ids_dict[person[1]] = person[0]

for line in sys.stdin:
    current_url = line.strip().split(';')[2].strip()
    current_person = line.strip().split(';')[0].strip()
    url = urllib.request.urlopen(current_url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')

    name = soup.main.div.text.strip().replace(' ', '_')

    if name:
        text = soup.main.get_text()
        if prep:
            text = text.lower()
            text = re.sub(punctuation, ' ', text)
            text = re.sub(regex, '', text)
            words = word_tokenize(text)
            words = [word for word in words if len(word) > 1]
            stop_words = stopwords.words('english')
            words = [word for word in words if word not in stop_words]
            stems = [porter.stem(word) for word in words]
            stems = ' '.join(stems)
            text = stems

        print(name)
        fname = name
        if current_person in ids_dict:
            fname = ids_dict[current_person]
        file = open(f'id_texts/{fname}', 'w+')
        file.write(text)
        file.close()
        print()
