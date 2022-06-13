#!./venv/bin/python3


import requests
from bs4 import BeautifulSoup
import string
import itertools
from multiprocessing import Pool
from Mathematician import Mathematician

id_link = 'https://www.genealogy.math.ndsu.nodak.edu/id.php?id={}'
prefix_link = 'https://www.genealogy.math.ndsu.nodak.edu/letter.php?letter={}'


def get_page_with_id(identifier):
    response = requests.get(id_link.format(identifier))
    return response.text


def search_family_name_prefix(prefix):
    url = "https://www.genealogy.math.ndsu.nodak.edu/query-prep.php"

    payload = 'chrono=0&given_name=&other_names=&family_name={}&school=&year=&thesis=&country=&msc=&submit=Submit'.format(
        prefix)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.genealogy.math.ndsu.nodak.edu',
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def get_with_prefix(prefix):
    r = requests.get(prefix_link.format(prefix))
    return r.text


def more_depth_is_needed(text):
    return "is too large" in text


def get_id_from_link(link):
    return link.attrs["href"].split("id=")[1]


def get_name_from_link(link):
    return link.string


def get_university_from_col(col):
    return col.text


def get_mathematician_from_row(row):
    cols = row.find_all('td')

    link = cols[0].find('a')
    identifier = get_id_from_link(link)
    name = get_name_from_link(link)
    university = get_university_from_col(cols[1])
    mathematician = Mathematician(identifier=identifier, full_name=name, university=university)
    # print(f"{id}\t\t{name}\t\t{university}")
    return mathematician


def extract_info_from_leaf_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.body.find('table')
    if rows is None:
        return []
    rows = rows.find_all('tr')
    return list(map(get_mathematician_from_row, rows))


def crawl_char_by_char(prefix):
    text = None
    if prefix:
        text = get_with_prefix(prefix)
    if not prefix or more_depth_is_needed(text):
        return list(itertools.chain.from_iterable(map(lambda c: crawl_char_by_char(prefix + c), string.ascii_uppercase)))
    else:
        # print(f"searching leaf {prefix}")
        return extract_info_from_leaf_page(text)


def crawl_by_search(prefix):
    try:
        text = search_family_name_prefix(prefix)
        return extract_info_from_leaf_page(text)
    except Exception as e:
        print(e)
        return []


def write_to_file(prefix, mathematicians):
    file = open(f"./names-and-ids/{prefix}.txt", "a")
    for mathematician in mathematicians:
        file.write("{}\t\t{}\t\t{}\n".format(mathematician.identifier, mathematician.full_name, mathematician.university))
    file.close()


def crawl_and_write_to_file(crawler, prefix):
    mathematicians = crawler(prefix)
    write_to_file(prefix, mathematicians)


def f(prefix):
    crawl_and_write_to_file(crawl_by_search, prefix)


def run():
    prefixes = [c1 + c2 for c1 in string.ascii_uppercase for c2 in string.ascii_uppercase]
    pool = Pool(processes=30)
    pool.map(f, prefixes)


def get_students_from_page(identifier):
    text = get_page_with_id(identifier)
    if "No students known" in text:
        return []
    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.body.find('table').find_all('tr')
    return list(map(get_mathematician_from_row, rows[1:]))


if __name__ == "__main__":
    run()
