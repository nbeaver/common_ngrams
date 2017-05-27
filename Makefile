.PHONY : all pep8

all:
	./common_words.py --include include/* --exclude exclude/*

pep8:
	pep8 common_words.py
