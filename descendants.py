#!./venv/bin/python3


import nltk
import unidecode
import re
from extract_ids import get_students_from_page


K = 5


class Mathmatician():

    def __init__(self, identifier, first_name, last_name):
        self.identifier = identifier
        self.first_name = first_name
        self.last_name = last_name

    def __lt__(self, mat):
        if mat.last_name != self.last_name:
            return self.first_name < mat.first_name
        return self.last_name < mat.last_name
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


def normalize(word):
    # remove accents
    word = unidecode.unidecode(word)

    # convert all chars to lowercase
    word = word.lower()
    return word

def get_file_lines():
    file_name = "all.txt"
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    return lines

def extract_names_and_family_names():
    mathmaticians = []
    lines = get_file_lines()
    for line in lines:
        identifier, full_name = line.split("\t\t")
        full_name = normalize(full_name) 
        splits = full_name.split(',')
        first_name = splits[-1].strip()
        last_name = splits[0].strip()

        mathmatician = Mathmatician(identifier, first_name, last_name)
        mathmaticians.append(mathmatician)

        m = re.match(".*,.*,.*", full_name)
        if m:
            pass
            # print(identifier, full_name)

    return mathmaticians


def levenstein_distance(a, b):
    a_len = len(a)
    b_len = len(b)

    d = [[0 for _ in range(b_len + 1)] for _ in range(a_len + 1)]

    for i in range(a_len):
        d[i][b_len] = a_len - i
    for i in range(b_len):
        d[a_len][i] = b_len - i

    for i in reversed(range(a_len)):
        for j in reversed(range(b_len)):
            if a[i] == b[j]:
                d[i][j] = d[i + 1][j + 1]
            else:
                d[i][j] = min(d[i + 1][j] + 1, d[i][j + 1] + 1)
    return d[0][0]



def find_best_matches(first_name, last_name, mathmaticians):
    f = lambda mathmatician: levenstein_distance(mathmatician.first_name, first_name) + levenstein_distance(mathmatician.last_name, last_name)
    g = lambda mathmatician: (f(mathmatician), mathmatician)

    candidates = list(sorted(map(g, mathmaticians)))
    return candidates[0:K]

def get_full_name():
    full_name = input("enter first name and last name seperated with a comma\n")
    if not ',' in full_name:
        print("you entered no ','")
        print("exiting")
        exit(1)
    return full_name

def find_best_candidates(full_name):
    first_name, last_name = full_name.split(',')
    first_name = first_name.strip()
    last_name = last_name.strip()
    mathmaticians = extract_names_and_family_names()
    best_candidates = find_best_matches(first_name, last_name, mathmaticians)
    return best_candidates


def prompt_for_best(best_candidates):
    print("candidates")
    for i, candidate in enumerate(best_candidates):
        print(i + 1, " ->", candidate[1])

    ind = int(input("enter index of best mathmatician you want"))
    return best_candidates[ind - 1][1]


def run():
    full_name = get_full_name()
    best_candidates = find_best_candidates(full_name)
    mathmatician = prompt_for_best(best_candidates)
    print(mathmatician.identifier)
    students = get_students_from_page(mathmatician.identifier)
    for student in students:
        print(student[0], student[1])


run()
