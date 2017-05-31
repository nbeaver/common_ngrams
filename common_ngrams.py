#! /usr/bin/env python3
from __future__ import print_function
import argparse
import nltk
import logging


def ngram_set(text, n):
    tokens = nltk.wordpunct_tokenize(text)
    return set(nltk.ngrams(tokens, n))


def ngrams_in_common(texts, n):
    ngram_sets = [ngram_set(text, n) for text in texts]
    common_ngrams = set(set.intersection(*ngram_sets))
    return common_ngrams


def ngrams_include_exclude(includes, excludes=[], n=1, nmax=10):
    exclude_ngrams = [ngram_set(exclude, n) for exclude in excludes]
    common_ngrams = ngrams_in_common(includes, n)
    for exclude_ngram_set in exclude_ngrams:
        common_ngrams = common_ngrams - exclude_ngram_set

    logging.info("{}-grams: {}".format(n, len(common_ngrams)))
    if len(common_ngrams) > 1 and n < nmax:
        return set.union(
            common_ngrams,
            ngrams_include_exclude(includes, excludes, n=n+1))
    else:
        return common_ngrams

def print_tuples_alphanumerically(iterable):
    for item in sorted(iterable):
        print(' '.join(item))

def print_tuples_longest_first(iterable):
    for item in sorted(iterable, key=lambda x: len(x), reverse=True):
        print(' '.join(item))


def get_texts(fp_list):
    texts = []
    if fp_list is None:
        return texts

    for fp in fp_list:
        try:
            text = fp.read()
        except UnicodeDecodeError:
            logging.error("Filename: {}".format(fp.name))
            raise
        texts.append(text)
    return texts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find n-grams in common for text files.')

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
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        dest='loglevel',
        const=logging.INFO,
        default=logging.WARNING
    )
    parser.add_argument(
        '-s',
        '--sort',
        choices=['alpha', 'length'],
        default='alpha',
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    include_texts = get_texts(args.include)
    exclude_texts = get_texts(args.exclude)

    ngrams = ngrams_include_exclude(include_texts, exclude_texts)

    if args.sort == 'alpha':
        print_tuples_alphanumerically(ngrams)
    elif args.sort == 'length':
        print_tuples_longest_first(ngrams)
    else:
        raise NotImplementedError
