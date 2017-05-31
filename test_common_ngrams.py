#! /usr/bin/env python3
import unittest
import common_ngrams
import nltk

class common_ngram_test(unittest.TestCase):

    def test_empty(self):
        example = "The quick brown fox jumps over the lazy dog."
        self.assertEqual(
            common_ngrams.ngrams_in_common(['', '']),
            set()
        )
        self.assertEqual(
            common_ngrams.ngrams_in_common(['', example]),
            set()
        )
        self.assertEqual(
            common_ngrams.ngrams_in_common([example, '']),
            set()
        )

    def test_same(self):
        example = set()
        example.add(tuple('I'))
        self.assertEqual(
            common_ngrams.ngrams_in_common(['I', 'I']),
            example
        )

    def test_disjoint(self):
        example = "The quick brown fox jumps over the lazy dog."
        disjoint = "Nothing from first sentence"
        self.assertEqual(
            common_ngrams.ngrams_in_common([example, disjoint]),
            set()
        )

if __name__ == '__main__':
    unittest.main()
