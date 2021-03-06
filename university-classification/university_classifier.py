import os
import re
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import unidecode

all_mathematicians_file_path = "all_mathematicians.txt"
id_files_path = "./processed_id_texts"

university_dict = {}
reputable_universities = []


def list_id_file_names():
    id_file_names = list(filter(lambda x: re.match(r"\d+", x), os.listdir(id_files_path)))
    x = list(filter(is_good_id, id_file_names))
    print(len(x), len(id_file_names))
    return x


def is_good_id(identifier):
    university_name = find_university_for_id(identifier)
    if university_name is None:
        return False
    return university_name in reputable_universities


def normalize(word):
    word = unidecode.unidecode(word)
    word = word.lower()
    return word


def load_reputable_universities():
    file = open("./pruned-unis.txt", "r")
    global reputable_universities
    reputable_universities = list(map(normalize, file.readlines()))
    file.close()


def establish_train_and_test_set(id_files):
    id_files_count = len(id_files)
    train_set = random.sample(population=id_files, k=600)
    test_set = set(id_files) - set(train_set)
    return train_set, test_set


def get_file_as_str(file_path):
    file = open(os.path.join(id_files_path, file_path), "r")
    return file.read()


def load_university_dict():
    file = open(all_mathematicians_file_path, "r")
    for line in file.readlines():
        items = line.split("\t\t")
        university = normalize(items[2])
        university_dict[items[0]] = university
    file.close()


def find_university_for_id(identifier):
    if identifier not in university_dict:
        return None

    university_name = university_dict[identifier]
    return university_name


count_vector = None
tfidf_transformer = None


def train(file_names):
    biographies = list(map(get_file_as_str, file_names))
    universities = list(map(find_university_for_id, file_names))

    global count_vector
    global tfidf_transformer

    count_vector = CountVectorizer(strip_accents='unicode', stop_words='english')
    x_train_counts = count_vector.fit_transform(biographies)

    tfidf_transformer = TfidfTransformer()
    x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)

    classifier = MultinomialNB().fit(x_train_tfidf, universities)
    return classifier


def test(file_names, classifier):
    biographies = list(map(get_file_as_str, file_names))
    real_universities = list(map(find_university_for_id, file_names))

    x_new_counts = count_vector.transform(biographies)

    x_new_tfidf = tfidf_transformer.transform(x_new_counts)

    predicted_universities = classifier.predict(x_new_tfidf)
    l = list(filter(lambda x: x[0] != x[1], zip(real_universities, predicted_universities)))
    print(len(l) / len(real_universities) * 100)


def run():
    load_university_dict()
    load_reputable_universities()
    id_file_names = list_id_file_names()
    train_set, test_set = establish_train_and_test_set(id_file_names)
    classifier = train(train_set)
    test(test_set, classifier)


run()
