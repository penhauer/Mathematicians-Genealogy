#!./venv/bin/python3


import requests
from bs4 import BeautifulSoup
import string
import re
import itertools
from multiprocessing import Pool


link = 'https://www.genealogy.math.ndsu.nodak.edu/letter.php?letter={}'


def get_with_prefix(prefix):
    r = requests.get(link.format(prefix))
    return r.text


def more_depth_is_needed(text):
    return "is too large" in text


def get_id_from_link(link):
    return link.attrs["href"].split("id=")[1]


def get_name_from_link(link):
    return link.string


def get_info_from_row(row):
    print("\n\n\n\n\n\n")
    print(row.text)
    cols = row.find_all('td') 

    link = cols[0].find('a')
    id = get_id_from_link(link) 
    name = get_name_from_link(link)
    return id, name 


def extract_info_from_leaf_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.body.find('table').find_all('tr')
    return list(map(get_info_from_row, rows))


def crawl(prefix):
    if prefix:
        text = get_with_prefix(prefix)
    if not prefix or more_depth_is_needed(text):
        return list(itertools.chain.from_iterable(map(lambda c: crawl(prefix + c), string.ascii_uppercase)))
    else:
        print(f"searching leaf {prefix}")
        return extract_info_from_leaf_page(text)


def crawl_and_write_to_file(prefix):
    items = crawl(prefix)
    f = open(f"./names-and-ids/{prefix}.txt", "a")
    for item in items:
        f.write("{}\t\t{}\n".format(item[0], item[1]))
    f.close()



prefix = input()
prefixes = list(map(lambda c: prefix + c, string.ascii_uppercase))
pool = Pool(processes=20)
pool.map(crawl_and_write_to_file, prefixes)
