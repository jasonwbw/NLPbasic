#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for class_tfidf.ClassTfIdf
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.class_tfidf import ClassTfIdf
import sys
import unittest

class ClassTfIdfTestCase(unittest.TestCase):
	def setUp(self):
		self.cdf = ClassTfIdf(3)
		for line in file("./nlp_basic/test/cdf_test.file"):
			_class, text = line.split("\t", 1)
			self.cdf.add_input_document(int(_class), text)
		self.cdf.compute_all_cdf()
		self.cdf.save_corpus_to_file("./nlp_basic/test/inverted.cdf")
		self.cdf.save_cdf_to_file("./nlp_basic/test/cdf.cdf")
		self.cdf = ClassTfIdf(3, corpus_filename = "./nlp_basic/test/inverted.cdf",\
			cdf_filename = "./nlp_basic/test/cdf.cdf")

	def tearDown(self):
		self.cdf = None

	def testGetNumDocs(self):
		self.assertEqual(3, self.cdf.get_num_docs(0))
		self.assertEqual(3, self.cdf.get_num_docs(1))
		self.assertEqual(3, self.cdf.get_num_docs(2))

	def testGetClasskeywords(self):
		self.assertEqual(['a'], self.cdf.get_class_keywords(0, 1))
		self.assertEqual(['b'], self.cdf.get_class_keywords(1, 1))
		self.assertEqual(['c'], self.cdf.get_class_keywords(2, 1))

	def testPrintSomething(self):
		pass

if __name__ == "__main__":  
    unittest.main() 