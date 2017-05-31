.PHONY : all pep8

all:
	./common_ngrams.py --verbose --include include/* --exclude exclude/*

pep8:
	pep8 common_ngrams.py
