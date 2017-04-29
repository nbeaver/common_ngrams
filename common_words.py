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
    args = parser.parse_args()
    setlist = []
    for included_file in args.include:
        setlist.append(wordset(included_file))

    common_words = set(set.intersection(*setlist))

    for word in sorted(common_words):
        sys.stdout.write(word + "\n")

    sys.stderr.write(str(len(common_words))+"\n")
