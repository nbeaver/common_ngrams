#! /usr/bin/env python3
from __future__ import print_function
import sys
import argparse
import nltk

def ngrams_in_common(includes, excludes, n=1, nmax=10):

    def tokenize(text):
        tokens = nltk.wordpunct_tokenize(text)
        return set(nltk.ngrams(tokens, n))

    def ngram_list(texts):
        return [tokenize(text) for text in texts]

    include_ngrams = ngram_list(includes)
    exclude_ngrams = ngram_list(excludes)
    common_ngrams = set(set.intersection(*include_ngrams))
    for exclude_ngram_set in exclude_ngrams:
        common_ngrams = common_ngrams - exclude_ngram_set

    sys.stderr.write('{}\n'.format(len(common_ngrams)))
    if len(common_ngrams) > 1 and n < nmax:
        return set.union(common_ngrams, ngrams_in_common(includes, excludes, n=n+1))
    else:
        return common_ngrams

def print_set_of_tuples(in_set):
    for item in sorted(in_set):
        print(' '.join(item))

def get_texts(fp_list):
    texts = []
    for fp in fp_list:
        try:
            text = fp.read()
        except UnicodeDecodeError:
            sys.stderr.write("Filename: {}\n".format(fp.name))
            raise
        texts.append(text)
    return texts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find n-grams in common for text files.')
    parser.add_argument(
        '-i', '--include',
        type=argparse.FileType('r'),
        nargs='+',
        help='Include n-grams from these files.',
        required=True,
    )
    parser.add_argument(
        '-x', '--exclude',
        type=argparse.FileType('r'),
        nargs='*',
        help='Exclude n-grams from these files.',
    )
    args = parser.parse_args()

    include_texts = get_texts(args.include)
    exclude_texts = get_texts(args.exclude)

    print_set_of_tuples(ngrams_in_common(include_texts, exclude_texts))
