#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for pmi.TopkHeap and PMIElement
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from pmi import TopkHeap
from pmi import PMIElement
from pmi import PMI
from inverted_index import InvertedIndex
import sys
import unittest
import math

class PMITestCase(unittest.TestCase):  
    def setUp(self):  
      self.iindex = InvertedIndex()
      for line in file("test.file"):
        self.iindex.add_input_document(line.strip())
      self.pmi = PMI(self.iindex, top = 2)
      self.pmi.build()
          
    def tearDown(self):  
      self.iindex = None
      self.pmi = None  
    
    def testTopPMI(self): 
      a = PMIElement('a', math.log(2/(4.0*5/5), 2))
      b = PMIElement('b', math.log(1/(4.0*1/5), 2))
      d = PMIElement('d', math.log(2/(4.0*3/5), 2))
      e = PMIElement('e', math.log(2/(4.0*4/5), 2))
      f = PMIElement('f', math.log(2/(4.0*5/5), 2))
      for i in self.pmi.get_top_pmi('c'):
        print i
      self.assertEqual(set([b, d]), set(self.pmi.get_top_pmi('c')))

    def testPrintSomething(self):
      pass

if __name__ == "__main__":  
    unittest.main()  
