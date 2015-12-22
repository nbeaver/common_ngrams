all:
	./common-words.py corpora/paper*
	./nltk-ngrams.py corpora/paper*
