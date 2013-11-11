#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for pmi.TopkHeap and PMIElement
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from pmi import TopkHeap
from pmi import PMIElement
import sys
import unittest

class TopkHeapTestCase(unittest.TestCase):  
    def setUp(self):  
      self.heap = TopkHeap(k = 2)
          
    def tearDown(self):  
      self.heap = None  
          
    def testInt(self): 
      # test the push and get all method for normal int
      b = 2   
      c = 3 
      d = 4  
      self.heap.push(b)
      self.assertEqual(set([b]), set(self.heap.topK()))
      self.heap.push(c)
      self.assertEqual(set([b, c]), set(self.heap.topK()))
      self.heap.push(d)
      self.assertEqual(set([c, d]), set(self.heap.topK()))

    def testPMIElement(self): 
      # test the push and get all method for PMIElement
      b = PMIElement('b', 2)    
      c = PMIElement('c', 3)    
      d = PMIElement('d', 3)    
      self.heap.push(b)
      self.assertEqual(set([b]), set(self.heap.topK()))
      self.heap.push(c)
      self.assertEqual(set([b, c]), set(self.heap.topK()))
      self.heap.push(d)
      self.assertEqual(set([c, d]), set(self.heap.topK()))

    def testPrintSomething(self):
      pass

if __name__ == "__main__":  
    unittest.main()  
