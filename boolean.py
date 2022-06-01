import glob

import pandas as pd

unique_words = set()
for file in glob.glob('texts/*'):
    print(file)
    file = open(file, "r")
    words = set(file.read().split())
    unique_words = unique_words.union(words)

print(unique_words)
