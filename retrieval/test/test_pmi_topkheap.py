#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for pmi.TopkHeap
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.topkheap import TopkHeap
from ..basic.pmi import PMIElement
import sys
import unittest

class TopkHeapTestCase(unittest.TestCase):  
    def setUp(self):  
      self.heap = TopkHeap(k = 2)
          
    def tearDown(self):  
      self.heap = None  
    
    def testPush(self):
      b = 2
      c = 3
      d = 4
      e = 1
      self.assertEqual(True, self.heap.push(b))
      self.assertEqual(True, self.heap.push(c))
      self.assertEqual(True, self.heap.push(d))
      self.assertEqual(False, self.heap.push(e))

    def testInt(self): 
      # test the push and get all method for normal int
      b = 2   
      c = 3 
      d = 4  
      self.heap.push(b)
      self.assertEqual(set([b]), set(self.heap.topk()))
      self.heap.push(c)
      self.assertEqual(set([b, c]), set(self.heap.topk()))
      self.heap.push(d)
      self.assertEqual(set([c, d]), set(self.heap.topk()))

    def testPMIElement(self): 
      # test the push and get all method for PMIElement
      b = PMIElement('b', 2)    
      c = PMIElement('c', 3)    
      d = PMIElement('d', 1) 
      f = PMIElement('d', 4)    
      self.heap.push(b)
      self.assertEqual([b], self.heap.topk())
      self.heap.push(c)
      self.assertEqual([c,b], self.heap.topk())
      self.heap.push(d)
      self.assertEqual([c, b], self.heap.topk())
      self.heap.push(f)
      self.assertEqual([f, c], self.heap.topk())

    def testPrintSomething(self):
      pass

if __name__ == "__main__":  
    unittest.main()  
