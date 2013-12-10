#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for pmi.MI
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.pmi import MI
from ..basic.pmi import PMI
from ..basic.inverted_index import InvertedIndex
import sys
import unittest
import math

class MITestCase(unittest.TestCase):  
    def setUp(self):  
    	self.iindex = InvertedIndex()
    	for line in file("./nlp_basic/test/test.file"):
    		self.iindex.add_input_document(line.strip())
    	self.pmi = PMI(self.iindex)
    	self.pmi.build()
    	self.mi = MI(self.iindex, self.pmi)

    def tearDown(self):  
    	self.iindex = None
    	self.pmi = None  
    
    def testComputeMI(self):
    	s1 = 'a d e'
    	s2 = 'b d c c'
    	res = 0.0
    	for t1 in s1.split():
    		for t2 in s2.split():
    			res += self.iindex.concurrence(t1, t2) / self.iindex.get_num_docs() * self.pmi.compute_pmi(t1, t2)
    	self.assertEqual(res, self.mi.compute_mi(s1.split(), s2.split()))

    def testPrintSomething(self):
    	pass

if __name__ == "__main__":  
    unittest.main()  
