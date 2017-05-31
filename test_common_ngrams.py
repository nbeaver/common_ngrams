#! /usr/bin/env python3
import unittest
import common_ngrams
import nltk

class ngrams_in_common(unittest.TestCase):

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

    def test_single_overlap(self):
        first = "The quick brown fox jumps"
        second = "jumps over the lazy dog."
        overlap = set()
        overlap.add(("jumps",))
        self.assertEqual(
            common_ngrams.ngrams_in_common([first, second], 1),
            overlap
        )

class ngrams_include_exclude(unittest.TestCase):
    def test_same(self):
        example = "The quick brown fox jumps over the lazy dog."
        self.assertEqual(
            common_ngrams.ngrams_include_exclude([example], [example]),
            set()
        )

    def test_almost_same(self):
        example1 = "The quick brown fox jumps over the lazy dog."
        example2 = "The quick brown fox jumps over the lazy dog"
        difference = set()
        difference.add(('.',))
        self.assertEqual(
            common_ngrams.ngrams_include_exclude([example1], [example2]),
            difference
        )

    def test_exclude_superset(self):
        example1 = "The quick brown fox jumps over the lazy dog"
        example2 = "The quick brown fox jumps over the lazy dog."
        self.assertEqual(
            common_ngrams.ngrams_include_exclude([example1], [example2]),
            set()
        )


class get_texts(unittest.TestCase):
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
