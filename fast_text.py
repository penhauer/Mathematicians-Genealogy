from pprint import pprint
from os.path import isfile
from os import listdir
from typing import Dict, List, Tuple

import fasttext
import numpy as np
from numpy import linalg as LA
from queries import subject_queries

MODEL_FILENAME = 'fasttext_model.bin'
VECTOR_SIZE = 100
DATA_DIR = './raw/'

def merge_biographies():
    filenames = listdir(DATA_DIR)
    with open('./merged.txt', 'w') as outfile:
        for fname in filenames:
            with open(f'{DATA_DIR}{fname}') as infile:
                for line in infile:
                    outfile.write(line)

def create_model():
    merge_biographies()
    model = fasttext.train_unsupervised('./merged.txt', 'skipgram')
    return model

def get_biography_vector(filname: str, model: fasttext.FastText._FastText) -> np.ndarray:
    res = np.array([0] * VECTOR_SIZE).astype('float64')
    length = 0
    with open(f'{DATA_DIR}{filname}', 'r') as f:
        for line in f:
            for word in line.split():
                length += 1
                vector = model.get_word_vector(word)
                res += vector
    return res / length

def get_biographies_vector(model: fasttext.FastText._FastText) -> Dict[str, np.ndarray]:
    res = dict()
    filenames = listdir(DATA_DIR)
    for filename in filenames:
        v = get_biography_vector(filname=filename, model=model)
        res[filename] = v
    return res

def get_similarity(v1: np.ndarray, v2: np.ndarray):
    return np.dot(v1, v2) / (LA.norm(v1) * LA.norm(v2))

def get_similarities(word: np.ndarray, vectors: Dict[str, np.ndarray]) -> List[Tuple[float, str]]:
    res = []
    for k, v in vectors.items():
        s = get_similarity(word, v)
        res.append((s, k))

    return res

def get_most_relevant_mathematicians(similarities: List[Tuple[float, str]], number_of_mathematicians: int = 5):
    res = sorted(similarities, key = lambda x: x[0])[-number_of_mathematicians:]
    res.reverse()
    return [name for _, name in res]

def print_result(res):
    for x in res:
        print(x)

if __name__ == '__main__':
    file_exists = isfile(MODEL_FILENAME)
    READ_FROM_STD = False
    if file_exists:
        model = fasttext.load_model(MODEL_FILENAME)
    else:
        model = create_model()
        model.save_model(MODEL_FILENAME)

    queries = []
    if READ_FROM_STD:
        queries.append(input('Enter your term: '))
    else:
        queries = subject_queries


    biography_vectors = get_biographies_vector(model=model)
    for query in queries:
        word_vector = model.get_word_vector(query)
        similarities = get_similarities(word_vector, biography_vectors)
        print(f'\n\nquery: {query}\n______________')
        print_result(get_most_relevant_mathematicians(similarities, 10))
