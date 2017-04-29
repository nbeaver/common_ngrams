#! /usr/bin/env python
import sys

def wordset(filename):
    with open(filename) as f:
        wordlist = f.read().split()
        wordlist_lower = [word.strip('.,"();"').lower() for word in wordlist]
    return set(wordlist_lower)

setlist = []
for filename in sys.argv[1:]:
    setlist.append(wordset(filename))

common_words = set(set.intersection(*setlist))

for word in sorted(common_words):
    sys.stdout.write(word + "\n")

sys.stderr.write(str(len(common_words))+"\n")
