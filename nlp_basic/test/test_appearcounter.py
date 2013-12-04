#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for appearcounter.AppearCount
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.appearcounter import AppearCount
import sys
import unittest

class AppearCountTestCase(unittest.TestCase):
	def setUp(self):
		self.ac = AppearCount()
		for line in file("./nlp_basic/test/test.file"):
			self.ac.add_input_document(line.strip())
		self.ac.init_file_count()
		for line in file("./nlp_basic/test/test.appearcount.file"):
			self.ac.count_file(line.strip())

	def tearDown(self):
		self.ac = None

	def testGetTermAppearCount(self):
		self.assertEqual(5, self.ac.get_term_appear_count('a'))
		self.assertEqual(0, self.ac.get_term_appear_count('b'))
		self.assertEqual(1, self.ac.get_term_appear_count('c'))
		self.assertEqual(4, self.ac.get_term_appear_count('d'))
		self.assertEqual(3, self.ac.get_term_appear_count('e'))
		self.assertEqual(4, self.ac.get_term_appear_count('f'))
		self.assertEqual(0, self.ac.get_term_appear_count('m'))

	def testGetTermAppearDocs(self):
		self.assertEqual(4, self.ac.get_term_appear_docs('a'))
		self.assertEqual(0, self.ac.get_term_appear_docs('b'))
		self.assertEqual(1, self.ac.get_term_appear_docs('c'))
		self.assertEqual(3, self.ac.get_term_appear_docs('d'))
		self.assertEqual(3, self.ac.get_term_appear_docs('e'))
		self.assertEqual(4, self.ac.get_term_appear_docs('f'))
		self.assertEqual(0, self.ac.get_term_appear_docs('m'))

	def testPrintSomething(self):
		pass

if __name__ == "__main__":  
    unittest.main() 