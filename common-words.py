#! /usr/bin/env python
import sys

setlist = []
for filename in sys.argv[1:]:
    f = open(filename, 'r')
    wordlist = f.read().split()
    wordlist_lower = [word.strip('.,"();"').lower() for word in wordlist]
    wordset = set(wordlist_lower)
    setlist.append(wordset)
    f.close()

common_words = sorted(set.intersection(*setlist))

for word in common_words:
    sys.stdout.write(word + "\n")

sys.stderr.write(str(len(common_words))+"\n")
