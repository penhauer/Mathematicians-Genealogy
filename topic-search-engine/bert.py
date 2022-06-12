import os
import pickle

import numpy as np

from typing import Dict, List, Tuple
from nltk import sent_tokenize
from numpy import linalg as LA
from sentence_transformers import SentenceTransformer

VECTOR_SIZE = 384
EMBEDDINGS_FILENAME = 'embeddings.pkl'


def get_biography_vector(filename: str, model: SentenceTransformer) -> np.ndarray:
    print(filename)
    res = np.zeros(VECTOR_SIZE)
    length = 0
    with open(f'./raw/{filename}', 'r') as f:
        for line in f:
            sentences = sent_tokenize(line)
            length += len(sentences)
            for sent in sentences:
                vector = model.encode([sent])[0]
                res += vector
    res /= length
    res /= LA.norm(res)
    return res


def get_biographies_vectors(model: SentenceTransformer) -> Dict[str, np.ndarray]:
    if os.path.isfile(EMBEDDINGS_FILENAME):
        with open(EMBEDDINGS_FILENAME, 'rb') as f:
            return pickle.load(f)
    res = dict()
    filenames = os.listdir('./raw/')
    for filename in filenames:
        v = get_biography_vector(filename=filename, model=model)
        res[filename] = v
    with open(EMBEDDINGS_FILENAME, 'wb+') as f:
        pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)
    return res


def get_similarity(v1: np.ndarray, v2: np.ndarray):
    return np.dot(v1, v2)


def get_similarities(word: np.ndarray, vectors: Dict[str, np.ndarray]) -> List[Tuple[float, str]]:
    res = []
    for k, v in vectors.items():
        s = float(get_similarity(word, v))
        res.append((s, k))
    return res


def get_most_relevant_mathematicians(similarities: List[Tuple[float, str]], number_of_mathematicians: int = 5):
    res = sorted(similarities, key=lambda x: x[0])[-number_of_mathematicians:]
    res.reverse()
    return [name for _, name in res]


if __name__ == '__main__':
    model = SentenceTransformer('all-MiniLM-L6-v2')
    biography_vectors = get_biographies_vectors(model=model)
    INPUT = input('Enter your term: ')
    while INPUT != 'exit':
        word_vector = model.encode([INPUT])[0]
        word_vector /= LA.norm(word_vector)

        similarities = get_similarities(word_vector, biography_vectors)
        ans = get_most_relevant_mathematicians(similarities, 10)
        ans = [name.replace('_', ' ') for name in ans]
        print(*ans, sep='\n')
        INPUT = input('Enter your term: ')
