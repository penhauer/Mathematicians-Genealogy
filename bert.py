from pprint import pprint
from os import listdir
from typing import Dict, List, Tuple

import numpy as np
from numpy import linalg as LA

from nltk import sent_tokenize
from sentence_transformers import SentenceTransformer

MODEL_FILENAME = 'fasttext_model.bin'
VECTOR_SIZE = 384


def get_biography_vector(filename: str, model: SentenceTransformer) -> np.ndarray:
    res = np.array([0] * VECTOR_SIZE).astype('float64')
    length = 0
    with open(f'./short/{filename}', 'r') as f:
        for line in f:
            for sent in sent_tokenize(line):
                vector = model.encode([sent])[0]
                length += 1
                res += vector
    return res / length


def get_biographies_vector(model: SentenceTransformer) -> Dict[str, np.ndarray]:
    res = dict()
    filenames = listdir('./short/')
    for filename in filenames:
        v = get_biography_vector(filename=filename, model=model)
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
    res = sorted(similarities, key=lambda x: x[0])[-number_of_mathematicians:]
    res.reverse()
    return [name for _, name in res]


if __name__ == '__main__':
    model = SentenceTransformer('all-MiniLM-L6-v2')
    INPUT = input('Enter your term: ')
    word_vector = model.encode([INPUT])[0]
    biography_vectors = get_biographies_vector(model=model)

    similarities = get_similarities(word_vector, biography_vectors)
    pprint(get_most_relevant_mathematicians(similarities, 4))
    print('end')
