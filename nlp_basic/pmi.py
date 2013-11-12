#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a simple PMI tool based on inverted_index
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from inverted_index import InvertedIndex
import heapq
import math

class PMIElement(object):
	def __init__(self, t2, pmi = 0):
		self.t2 = t2
		self.pmi = pmi

	def __gt__(self, element):
		if isinstance(element, PMIElement):
			return self.pmi > element.pmi
		raise TypeError

	def __eq__(self, other):  
		if isinstance(other, PMIElement) and \
			other.t2 == self.t2 and other.pmi == self.pmi:
			return True
		return False

	def __str__(self):
		return self.t2 + ":" + str(self.pmi)


class TopkHeap(object):
    def __init__(self, k = 50):
        self.k = k
        self.data = []

    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem) 

    def topK(self):
    	return sorted(self.data)[::-1]
    	# tem_data = self.data
        # return [x for x in reversed([heapq.heappop(tem_data) for x in xrange(len(tem_data))])]


class PMI(object):
	def __init__(self, inverted_index, top = 50):
		self.iindex = inverted_index
		self.top = top
		self.term_pmi = {}

	def change_inverted_index(self, inverted_index):
		self.inverted_index = inverted_index

	def build(self):
		inf = -float('inf')
		terms = self.iindex.get_terms()
		for term in terms:
			self.term_pmi[term] = TopkHeap(self.top)
		for i in range(len(terms)-1):
			for j in range(i+1, len(terms)):
				# PMI(t1, t2) = log(p(t1,t2)/(p(t1)p(t2)))
				to_log = self.iindex.concurrence(terms[i], terms[j]) \
					/(self.iindex.get_word_appear(terms[i]) \
						* self.iindex.get_word_appear(terms[j]) \
						/ self.iindex.get_num_docs())
				if to_log == 0:
					pmi = inf
				else:
					pmi = math.log(to_log,  2)
				self.term_pmi[terms[i]].push(PMIElement(terms[j], pmi))
				self.term_pmi[terms[j]].push(PMIElement(terms[i], pmi))

	def get_top_pmi(self, term):
		return self.term_pmi[term].topK()
