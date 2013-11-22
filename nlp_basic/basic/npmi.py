#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a simple NPMI tool based on inverted_index
#
# Reference: http://en.wikipedia.org/wiki/Pointwise_mutual_information 
# Paper: Normalized(Pointwise) Mutual Information in Collocation Extraction
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from pmi import PMI
import math

class NPMI(PMI):

	def compute_pmi(self, t1 , t2):
		# NPMI(t1, t2) = log(p(t1,t2)/(p(t1)p(t2))) / -log(p(t1,t2))
		to_log = self.iindex.concurrence(t1, t2) * self.iindex.get_num_docs()\
			/(self.iindex.get_word_appear(t1) \
			* self.iindex.get_word_appear(t2))
		if to_log == 0:
			return -1

		p_t1_t2 = math.log(self.iindex.concurrence(t1, t2) \
		    /(self.iindex.get_num_docs()), 2)
		if p_t1_t2 == 0:
			return 1
		else:
			return -math.log(to_log,  2) / p_t1_t2

	def get_top_pmi(self, term):
		return [i for i in super(NPMI,self).get_top_pmi(term)