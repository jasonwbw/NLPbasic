#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for npmi.NPMI
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.topkheap import TopkHeap
from ..basic.pmi import PMIElement
from ..basic.npmi import NPMI
from ..basic.inverted_index import InvertedIndex
import sys
import unittest
import math

class NPMITestCase(unittest.TestCase):  
    def setUp(self):  
      self.iindex = InvertedIndex()
      for line in file("./nlp_basic/test/test.file"):
        self.iindex.add_input_document(line.strip())
      self.pmi = NPMI(self.iindex, top = 2)
      self.pmi.build()
          
    def tearDown(self):  
      self.iindex = None
      self.pmi = None  
    
    def testTopPMI(self): 
      # with c
      a = PMIElement('a', -math.log(2*5/(2.0*5), 2)/math.log(2.0/5, 2))
      b = PMIElement('b', -math.log(1*5/(2.0*1), 2)/math.log(1.0/5, 2))
      d = PMIElement('d', -math.log(2*5/(2.0*3), 2)/math.log(2.0/5, 2))
      e = PMIElement('e', -math.log(2*5/(2.0*4), 2)/math.log(2.0/5, 2))
      f = PMIElement('f', -math.log(2*5/(2.0*5), 2)/math.log(2.0/5, 2))
      for i in range(len(self.pmi.get_top_pmi('c'))):
        if i == 0:
          self.assertEqual(b, self.pmi.get_top_pmi('c')[i])
        else:
          self.assertEqual(d, self.pmi.get_top_pmi('c')[i])

    def testPrintSomething(self):
      pass

if __name__ == "__main__":  
    unittest.main()  
