#!./venv/bin/python3

import unidecode
from .extract_ids import get_students_from_page
from .Mathematician import Mathematician


K = 5


def normalize(word):
    # remove accents
    word = unidecode.unidecode(word)

    # convert all chars to lowercase
    word = word.lower()
    return word


def get_file_lines():
    file_name = "all_mathematicians.txt"
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    return lines


def extract_names_and_family_names():
    mathematicians = []
    lines = get_file_lines()
    for line in lines:
        identifier, full_name, university = line.split("\t\t")
        full_name = normalize(full_name)
        splits = full_name.split(',')
        first_name = splits[-1].strip()
        last_name = splits[0].strip()

        mathematician = Mathematician(identifier=identifier, first_name=first_name, last_name=last_name, full_name=full_name, university=university)
        mathematicians.append(mathematician)

    return mathematicians


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


def find_best_matches(first_name, last_name, mathematicians):
    dis = lambda mathematician: \
        levenstein_distance(mathematician.first_name, first_name) + \
        levenstein_distance(mathematician.last_name, last_name)
    g = lambda mathematician: (dis(mathematician), mathematician)

    candidates = list(sorted(map(g, mathematicians)))
    return candidates[0:K]


def get_full_name():
    full_name = input("enter first name and last name seperated with a comma\n")
    if ',' not in full_name:
        print("you entered no ','")
        print("exiting")
        exit(1)
    return full_name


def find_best_candidates(full_name):
    first_name, last_name = full_name.split(',')
    first_name = first_name.strip()
    last_name = last_name.strip()
    mathematicians = extract_names_and_family_names()
    best_candidates = find_best_matches(first_name, last_name, mathematicians)
    return best_candidates


def prompt_for_best(best_candidates):
    print("candidates")
    for i, candidate in enumerate(best_candidates):
        print(i + 1, " ->", candidate[1])

    ind = int(input("enter index of best mathematician you want\n"))
    return best_candidates[ind - 1][1]


def run():
    full_name = get_full_name()
    best_candidates = find_best_candidates(full_name)
    mathematician = prompt_for_best(best_candidates)
    print(mathematician.identifier)
    students = get_students_from_page(mathematician.identifier)
    if students:
        for student in students:
            print(student)
    else:
        print("No students known.")


run()
