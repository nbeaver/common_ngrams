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

def words_in_common(included_fp, excluded_fp, tokenizer):
    include_words = []
    for included_fp in included_fp:
        include_words.append(tokenizer(included_fp))
    exclude_words = []
    for excluded_fp in excluded_fp:
        exclude_words.append(tokenizer(excluded_fp))
    common_words = set(set.intersection(*include_words))
    for exclude_wordset in exclude_words:
        common_words = common_words - exclude_wordset
    return common_words

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

    display_words = words_in_common(args.include, args.exclude, word_set)
    print_set(display_words)

    display_bigrams = words_in_common(args.include, args.exclude, bigram_set)
    print_set(display_bigrams)
