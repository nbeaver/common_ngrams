#! /usr/bin/env python3
from __future__ import print_function
import argparse
import logging
import re
import os.path

def tokenize(text, lowercase=False):
    # Based on wordpunkt tokenize in NLTK.
    # https://github.com/nltk/nltk/blob/21b4d0af6f7e94ba49b3d912c9d64564082db440/nltk/tokenize/regexp.py#L183
    pattern = r'\w+|[^\w\s]+'
    regexp = re.compile(pattern)
    tokens_raw = regexp.findall(text)
    if lowercase:
        tokens = [t.lower() for t in tokens_raw]
    else:
        tokens = tokens_raw
    return tokens

def ngram_set(text, n, lowercase=False):
    import nltk
    tokens = tokenize(text, lowercase)
    ngrams = set(nltk.ngrams(tokens, n))
    return ngrams

def ngrams_in_common(texts, n, lowercase=False):
    ngram_sets = [ngram_set(text, n, lowercase) for text in texts]
    common_ngrams = set(set.intersection(*ngram_sets))
    return common_ngrams


def ngrams_include_exclude(includes, excludes=[], n=1, nmax=10, lowercase=False):
    exclude_ngrams = [ngram_set(exclude, n, lowercase) for exclude in excludes]
    common_ngrams = ngrams_in_common(includes, n, lowercase)
    for exclude_ngram_set in exclude_ngrams:
        common_ngrams = common_ngrams - exclude_ngram_set

    logging.info("{}-grams: {}".format(n, len(common_ngrams)))
    if len(common_ngrams) > 1 and n < nmax:
        return set.union(
            common_ngrams,
            ngrams_include_exclude(includes, excludes, n=n+1, nmax=nmax, lowercase=lowercase))
    else:
        return common_ngrams

def print_tuples_alphanumerically(iterable):
    for item in sorted(iterable):
        print(' '.join(item))

def print_tuples_longest_first(iterable):
    for item in sorted(iterable, key=lambda x: len(x), reverse=True):
        print(' '.join(item))


def get_fps(path_list):
    # TODO: re-work this
    fp_list = []
    if path_list is None:
        return fp_list

    for path in path_list:
        fp = open(path, encoding='utf-8')
        fp_list.append(fp)

    return fp_list

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

def existing_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError('path does not exist: {}'.format(path))
    elif not os.path.isfile(path):
        raise FileNotFoundError('not a file: {}'.format(path))
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find n-grams in common for text files.')

    parser.add_argument(
        '-i', '--include',
        type=existing_file,
        nargs='+',
        help='Include n-grams from these files.',
        required=True,
    )
    parser.add_argument(
        '-x', '--exclude',
        type=existing_file,
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
        '-l',
        '--lowercase',
        action='store_true',
        help='Use all lowercase (case-insensitive matching)',
    )
    parser.add_argument(
        '-s',
        '--sort',
        choices=['alpha', 'length'],
        default='alpha',
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    include_fps = get_fps(args.include)
    exclude_fps = get_fps(args.exclude)
    include_texts = get_texts(include_fps)
    exclude_texts = get_texts(exclude_fps)

    ngrams = ngrams_include_exclude(include_texts, exclude_texts, lowercase=args.lowercase)

    if args.sort == 'alpha':
        print_tuples_alphanumerically(ngrams)
    elif args.sort == 'length':
        print_tuples_longest_first(ngrams)
    else:
        raise NotImplementedError
