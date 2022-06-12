import string
import urllib.request

from bs4 import BeautifulSoup

BASE_URL = 'https://mathshistory.st-andrews.ac.uk/Biographies/letter-'
ALPHABET = list(string.ascii_lowercase)

for letter in ALPHABET:
    current_url = f'{BASE_URL}{letter}/'
    url = urllib.request.urlopen(current_url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')

    for x in soup.find_all('div', attrs={'class': 'col'}):
        for y in x.find_all('li'):
            for z in y.find_all('a'):
                print(z.string.strip(), ';', y.contents[1].strip(), ';', f'{current_url}{z.get("href")}')
