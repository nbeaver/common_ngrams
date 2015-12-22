#! /usr/bin/env python3

import sys
import nltk

bigram_sets = []
trigram_sets = []
for filename in sys.argv[1:]:
    text = open(filename).read()
    tokens = nltk.wordpunct_tokenize(text)
    bigram_sets.append(set(nltk.ngrams(tokens, 2)))
    trigram_sets.append(set(nltk.ngrams(tokens, 3)))

bigrams_in_every_file = sorted(set(set.intersection(*bigram_sets)))
trigrams_in_every_file = sorted(set(set.intersection(*trigram_sets)))

for a, b in bigrams_in_every_file:
    print(a,b)

for a, b, c in trigrams_in_every_file:
    print(a,b, c)
