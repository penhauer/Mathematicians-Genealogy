#!./venv/bin/python3


import requests
from bs4 import BeautifulSoup
import string
import re
import itertools

         

link = 'https://www.genealogy.math.ndsu.nodak.edu/letter.php?letter={}'
id_link = 'https://www.genealogy.math.ndsu.nodak.edu/id.php?id={}'



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


def get_page_with_id(mathmatician_id):
    r = requests.get(id_link.format(mathmatician_id))
    return r.text

def extract_info_from_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    def extract_name():
        return soup.find_all("h2")[0].text.strip("\n").strip(" ")

    def extract_year():
        year_element = soup.find('div', attrs={'style':'line-height: 30px; text-align: center; margin-bottom: 1ex'})
        year = year_element.find_all('span')[0].contents[-1].strip(" ")
        return year

    def extract_advisors():
        paragraphs = soup.find_all("p")
        advisors = [p for p in paragraphs if "Advisor" in p.text][0]
        advisors = list(map(get_id_from_link, advisors.find_all("a")))
        return advisors


    name = extract_name()
    year = extract_year()
    advisors = extract_advisors()
    return name, year, advisors

def page_exists(text):
    return not "You have specified an ID that does not exist in the database" in text


def check_pages():
    for i in range(5):
        text = get_page_with_id(i)
        if page_exists(text):
            extract_info_from_page(text)

s = input()
items = crawl(s)
f = open("output.txt", "a")
for item in items:
    f.write("{} {}\n".format(item[0], item[1]))
f.close()

