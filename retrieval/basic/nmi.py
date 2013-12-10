#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a simple NMI tool based on MI
#
# Reference: http://en.wikipedia.org/wiki/Pointwise_mutual_information 
# Paper: Normalized(Pointwise) Mutual Information in Collocation Extraction
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from pmi import MI
import math

class NMI(MI):

	def compute_mi(self, sentence1, sentence2):
		# NMI(t1, t2) = mi / -sum_x_y_in_s12( p(x, y)logp(x, y))
		mi = MI.compute_mi(self, sentence1, sentence2)
		denominator = 0.0
		for t1 in sentence1:
			for t2 in sentence2:
				p = self.iindex.concurrence(t1, t2) / self.iindex.get_num_docs()
				if p > 0:
					denominator += p * math.log(p, 2)
		return mi != 0 and -mi / denominator or 0