#! /usr/bin/env python3
import unittest
import common_ngrams
import nltk

class common_ngram_test(unittest.TestCase):

    def test_empty(self):
        example = "The quick brown fox jumps over the lazy dog."
        self.assertEqual(
            common_ngrams.ngrams_in_common(['', ''], 1),
            set()
        )
        self.assertEqual(
            common_ngrams.ngrams_in_common(['', example], 1),
            set()
        )
        self.assertEqual(
            common_ngrams.ngrams_in_common([example, ''], 1),
            set()
        )

    def test_same(self):
        example = set()
        example.add(tuple('I'))
        self.assertEqual(
            common_ngrams.ngrams_in_common(['I', 'I'], 1),
            example
        )

    def test_disjoint(self):
        example = "The quick brown fox jumps over the lazy dog."
        disjoint = "Nothing from first sentence"
        for n in range(1, len(nltk.wordpunct_tokenize(example))+1):
            self.assertEqual(
                common_ngrams.ngrams_in_common([example, disjoint], n),
                set()
            )

class get_texts_test(unittest.TestCase):
    import tempfile
    myfile1 = tempfile.NamedTemporaryFile()
    myfile1.file.write(bytes('test1', encoding='utf-8'))
    myfile1.file.seek(0)
    myfile2 = tempfile.NamedTemporaryFile()
    myfile2.file.write(bytes('test2', encoding='utf-8'))
    myfile2.file.seek(0)
    fp_list = [myfile1.file, myfile2.file]
    common_ngrams.get_texts(fp_list)

if __name__ == '__main__':
    unittest.main()
