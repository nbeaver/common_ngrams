#! /usr/bin/env python
import sys
import argparse

def wordset(fp):
    wordlist = fp.read().split()
    wordlist_lower = [word.strip('.,"();"').lower() for word in wordlist]
    return set(wordlist_lower)

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
    include_words = []
    for included_file in args.include:
        include_words.append(wordset(included_file))

    exclude_words = []
    for excluded_file in args.exclude:
        exclude_words.append(wordset(excluded_file))

    common_words = set(set.intersection(*include_words))

    for exclude_wordset in exclude_words:
        common_words = common_words - exclude_wordset

    for word in sorted(common_words):
        sys.stdout.write(word + "\n")

    sys.stderr.write(str(len(common_words))+"\n")
