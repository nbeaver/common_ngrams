.PHONY : all pep8

all:
	./common_ngrams.py --include include/* --exclude exclude/*

pep8:
	pep8 common_ngrams.py
