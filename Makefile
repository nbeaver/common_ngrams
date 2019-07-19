PY = $(wildcard *.py)
.PHONY : all pep8 test

all:
	./common_ngrams.py --verbose --include include/* --exclude exclude/*

lowercase:
	./common_ngrams.py --lowercase --verbose --include include/* --exclude exclude/*

test:
	./test_common_ngrams.py

pep8:
	pep8 $(PY)
