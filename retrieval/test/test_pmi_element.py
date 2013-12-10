#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The unit test case for pmi.PMIElement
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..basic.pmi import PMIElement
import sys
import unittest

class PMIElementTestCase(unittest.TestCase):  
    def setUp(self):  
      pass
          
    def tearGt(self):  
      f = PMIElement('f', 12)
      e = PMIElement('e', 11)
      self.assertEqual(True, e < f)
      self.assertEqual(True, f > e)
    
    def testEq(self): 
      f = PMIElement('f', 11)
      e = PMIElement('e', 11)
      g = PMIElement('e', 11)
      self.assertEqual(False, e == f)
      self.assertEqual(True, e == g)


    def testPrintSomething(self):
      pass

if __name__ == "__main__":  
    unittest.main()  
