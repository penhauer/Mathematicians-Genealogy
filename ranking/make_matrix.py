from asyncore import read
import os, re
from typing import List, Set
from os.path import isfile
from os import listdir
from typing import Dict, List, Tuple
import string

from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords

import fasttext
import numpy as np
from numpy import int32, linalg as LA

from ranking import do_ranking

DATA_DIR = './topic-search-engine/summary_texts/'
PREPROCESSED_DATA_DIR = './preprocessed_data/'
MODEL_FILENAME = 'fasttext_model_summary.bin'
VECTOR_SIZE = 100

def get_common_words(s1:str, s2:str) -> Set[str]:
    str1_words = set(s1.split())
    str2_words = set(s2.split())
    common = str1_words & str2_words
    return common

def get_file_names(path: str) -> List[str]:
    res = []
    file_names = os.listdir(DATA_DIR)
    for file_name in file_names:
        if not file_name.isnumeric():
            res.append(file_name)
    return res

def merge_biographies():
    filenames = get_file_names(DATA_DIR)
    output_filename = './merged.txt'
    with open(output_filename, 'w') as outfile:
        for fname in filenames:
            with open(f'{DATA_DIR}{fname}') as infile:
                for line in infile:
                    outfile.write(line)
    return output_filename

def create_model():
    output_filename = merge_biographies()
    model = fasttext.train_unsupervised(output_filename, 'skipgram')
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
    filenames = get_file_names(DATA_DIR)
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

def get_similaritiy_common_word(filename1: str, filename2: str, preprocess_: bool):
    if preprocess_:
        with open(f'{PREPROCESSED_DATA_DIR}{filename1}', 'r') as f1:
            with open(f'{PREPROCESSED_DATA_DIR}{filename2}', 'r') as f2:
                content1 = f1.read()
                content2 = f2.read()

                commons = get_common_words(content1, content2)
                return len(commons)
    else:
        with open(f'{DATA_DIR}{filename1}', 'r') as f1:
            with open(f'{DATA_DIR}{filename2}', 'r') as f2:
                content1 = f1.read()
                content2 = f2.read()

                commons = get_common_words(content1, content2)
                return len(commons)

def get_most_relevant_mathematicians(similarities: List[Tuple[float, str]], number_of_mathematicians: int = 5):
    res = sorted(similarities, key = lambda x: x[0])[-number_of_mathematicians:]
    res.reverse()
    return [name for _, name in res]

def print_result(res):
    for x in res:
        print(x)

def preprocess(text: str):
    text = text.lower()
    text = re.sub(punctuation, ' ', text)
    text = re.sub(regex, '', text)
    words = word_tokenize(text)
    words = [word for word in words if len(word) > 1]
    stop_words = stopwords.words('english')
    words = [word for word in words if word not in stop_words]
    stems = [porter.stem(word) for word in words]
    stems = ' '.join(stems)
    text = stems

    return text

def preprocess_summaries(input_path:str, output_path:str):
    filenames = get_file_names(input_path)
    for filename in filenames:
        with open(f'{input_path}{filename}', 'r') as f:
            content = f.read()
            preprocessed_content = preprocess(content)
            output = open(f'{output_path}{filename}', 'w+')
            output.write(preprocessed_content)


if __name__ == '__main__':
    regex = re.compile(r'[^a-z\s]')
    punctuation = re.compile('[' + string.punctuation + ']')
    porter = PorterStemmer()

    file_exists = isfile(MODEL_FILENAME)
    READ_FROM_STD = False
    if file_exists:
        model = fasttext.load_model(MODEL_FILENAME)
    else:
        model = create_model()
        model.save_model(MODEL_FILENAME)

    # biography_vectors = get_biographies_vector(model=model)
    # for name in list(biography_vectors.keys()):
    #     similarities = get_similarities(biography_vectors[name], biography_vectors)
    #     res = []
    #     for s, target_name in similarities:
    #         if target_name == name:
    #             continue
            # if s > 0.99999:
    #             res.append(s)
    #             print(f'\t{target_name}')
    #     print(len(res), name)
    # #     word_vector = model.get_word_vector(query)

    filenames = get_file_names(DATA_DIR)
    MATRIX_SIZE = 1700
    matrix = np.zeros(len(filenames[:MATRIX_SIZE]) ** 2).astype(int32)
    matrix = matrix.reshape(len(filenames[:MATRIX_SIZE]), len(filenames[:MATRIX_SIZE]))

    for i, filename1 in enumerate(filenames[:MATRIX_SIZE]):
        for j, filename2 in enumerate(filenames[:MATRIX_SIZE]):
            if i == j:
                continue
            s = get_similaritiy_common_word(filename1, filename2, False)
            if s > 4:
                matrix[i][j] = 1
    print(matrix)
    do_ranking(matrix)
