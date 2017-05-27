#! /usr/bin/env python3
from __future__ import print_function
import sys
import argparse
import nltk

def unigram_set(text):
    tokens = nltk.wordpunct_tokenize(text)
    return set(nltk.ngrams(tokens, 1))

def bigram_set(text):
    tokens = nltk.wordpunct_tokenize(text)
    return set(nltk.ngrams(tokens, 2))

def trigram_set(text):
    tokens = nltk.wordpunct_tokenize(text)
    return set(nltk.ngrams(tokens, 3))

def ngrams_in_common(include_list, exclude_list, tokenizer):
    include_ngrams = []
    for include in include_list:
        include_ngrams.append(tokenizer(include))
    exclude_ngrams = []
    for exclude in exclude_list:
        exclude_ngrams.append(tokenizer(exclude))
    common_ngrams = set(set.intersection(*include_ngrams))
    for exclude_ngram_set in exclude_ngrams:
        common_ngrams = common_ngrams - exclude_ngram_set
    return common_ngrams

def print_set(in_set):
    for item in sorted(in_set):
        print(' '.join(item))
    sys.stderr.write('{} ------------------------\n'.format(len(in_set)))

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
    parser = argparse.ArgumentParser(description='Find words in common for some text files.')
    parser.add_argument(
        '-i', '--include',
        type=argparse.FileType('r'),
        nargs='+',
        help='Include words from these files.',
        required=True,
    )
    parser.add_argument(
        '-x', '--exclude',
        type=argparse.FileType('r'),
        nargs='*',
        help='Exclude words from these files.',
    )
    args = parser.parse_args()

    include_texts = get_texts(args.include)
    exclude_texts = get_texts(args.exclude)

    tokenizer_funcs = [
        unigram_set,
        bigram_set,
        trigram_set,
    ]

    for tokenizer_func in tokenizer_funcs:
        print_set(ngrams_in_common(include_texts, exclude_texts, tokenizer_func))
