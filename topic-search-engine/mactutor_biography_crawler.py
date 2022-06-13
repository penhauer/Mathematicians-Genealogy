from enum import Enum
import re
import string
import sys
import urllib.request

from nltk.stem.porter import PorterStemmer
from tqdm import tqdm
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords


def get_summary(url: str):
    url = urllib.request.urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    res = soup.find_all('span', {'class': 'markup'})[0]
    return res.text

def get_all(url: str):
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    text = soup.main.get_text()
    return text

def get_name(url: str):
    url = urllib.request.urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')

    name = soup.main.div.text.strip().replace(' ', '_')
    return name

def preprocess(text: str):
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

    return text

class ParsingMode(Enum):
    SIMPLE = 1
    SUMMARY = 2

PARSING_MODE = ParsingMode.SUMMARY
OUTPUT_DIR = 'summary_texts'

if __name__ == "__main__":
    regex = re.compile(r'[^a-z\s]')
    punctuation = re.compile('[' + string.punctuation + ']')
    porter = PorterStemmer()

    prep = False
    if len(sys.argv) > 1:
        prep = sys.argv[1] == 'y'
    print(f'preprocess: {prep}')

    ids_dict = {}
    with open('ids.txt', 'r') as f:
        for line in f:
            person = line.strip().split('\t')
            ids_dict[person[1]] = person[0]

    for line in sys.stdin:
        url = line.strip().split(';')[2].strip()
        current_person = line.strip().split(';')[0].strip()
        name = get_name(url)

        if name:
            if PARSING_MODE == ParsingMode.SIMPLE:
                text = get_all(url)
            elif PARSING_MODE == ParsingMode.SUMMARY:
                text = get_summary(url)

            if prep:
                text = preprocess(text)

            print(name)
            fname = name
            if current_person in ids_dict:
                fname = ids_dict[current_person]
            file = open(f'{OUTPUT_DIR}/{fname}', 'w+')
            file.write(text)
            file.close()
            print()
