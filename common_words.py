#! /usr/bin/env python
import sys
import argparse


def wordset(fp):
    wordlist = fp.read().split()
    wordlist_lower = [word.strip('.,"();"').lower() for word in wordlist]
    return set(wordlist_lower)


def words_in_common(included_fp, excluded_fp):
    include_words = []
    for included_fp in included_fp:
        include_words.append(wordset(included_fp))
    exclude_words = []
    for excluded_fp in excluded_fp:
        exclude_words.append(wordset(excluded_fp))
    common_words = set(set.intersection(*include_words))
    for exclude_wordset in exclude_words:
        common_words = common_words - exclude_wordset
    return common_words


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

    display_words = words_in_common(args.include, args.exclude)

    for word in sorted(display_words):
        sys.stdout.write(word + "\n")
