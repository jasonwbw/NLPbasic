#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for inverted_index.InvertedIndex
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.inverted_index import InvertedIndex
import sys
import unittest

class InvertedIndexTestCase(unittest.TestCase):  
    def setUp(self):  
      self.iindex = InvertedIndex()
      for line in file("test.file"):
        self.iindex.add_input_document(line.strip())
      self.iindex.save_corpus_to_file("inverted.index")
      self.iindex.load_corpus_from_file("inverted.index")
          
    def tearDown(self):  
      self.iindex = None  
          
    def testGetNumDocs(self):      
      self.assertEqual(5, self.iindex.get_num_docs())

    def testConcurrence(self):
      self.assertEqual(5, self.iindex.concurrence('a', 'f'))
      self.assertEqual(4, self.iindex.concurrence('a', 'e'))
      self.assertEqual(3, self.iindex.concurrence('d', 'e'))
      self.assertEqual(1, self.iindex.concurrence('b', 'e'))
      self.assertEqual(0, self.iindex.concurrence('a', 'g'))

    def testGetWordAppear(self):
      # added for smoothness
      self.assertEqual(5, self.iindex.get_word_appear('a'))
      self.assertEqual(4, self.iindex.get_word_appear('e'))
      self.assertEqual(3, self.iindex.get_word_appear('d'))
      self.assertEqual(1, self.iindex.get_word_appear('b'))

    def testGetTerms(self):
      self.assertEqual(set(['a', 'b', 'c', 'd', 'e', 'f']), set(self.iindex.get_terms()))

    def testTopKAppear(self):
      self.assertEqual([(5.0, 'f'), (5.0, 'a'), (4.0, 'e')], self.iindex.top_k_appear(3))

    def testPrintSomething(self):
      for i in self.iindex:
        print "InvertedIndexTestCase.testPrintSomething.case1:", i

if __name__ == "__main__":  
    unittest.main()  
