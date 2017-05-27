#! /usr/bin/env python3
from __future__ import print_function
import sys
import argparse
import nltk

def word_set(fp):
    wordlist = fp.read().split()
    wordlist_lower = [word.strip('.,"();"').lower() for word in wordlist]
    return set(wordlist_lower)

def bigram_set(fp):
    tokens = nltk.wordpunct_tokenize(fp.read())
    return set(nltk.ngrams(tokens, 2))

def trigram_set(fp):
    tokens = nltk.wordpunct_tokenize(fp.read())
    return set(nltk.ngrams(tokens, 3))

def ngrams_in_common(included_fp, excluded_fp, tokenizer):
    include_ngrams = []
    for included_fp in included_fp:
        include_ngrams.append(tokenizer(included_fp))
    exclude_ngrams = []
    for excluded_fp in excluded_fp:
        exclude_ngrams.append(tokenizer(excluded_fp))
    common_ngrams = set(set.intersection(*include_ngrams))
    for exclude_ngram_set in exclude_ngrams:
        common_ngrams = common_ngrams - exclude_ngram_set
    return common_ngrams

def print_set(in_set):
    for item in sorted(in_set):
        print(str(item))
    sys.stderr.write('{}\n'.format(len(in_set)))

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

    display_words = ngrams_in_common(args.include, args.exclude, word_set)
    print_set(display_words)

    display_bigrams = ngrams_in_common(args.include, args.exclude, bigram_set)
    print_set(display_bigrams)

    display_trigrams = ngrams_in_common(args.include, args.exclude, trigram_set)
    print_set(display_trigrams)
