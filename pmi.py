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
		return self.pmi > element.pmi


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
    	return sorted(self.data)
    	# tem_data = self.data
        # return [x for x in reversed([heapq.heappop(tem_data) for x in xrange(len(tem_data))])]


class PMI(object):
	def __init__(self, inverted_index, top = 50):
		self.inverted_index = inverted_index
		self.top = top
		self.term_pmi = {}

	def change_inverted_index(self, inverted_index):
		self.inverted_index = inverted_index

	def build(self):
		terms = self.inverted_index.get_terms()
		for term in terms:
			self.term_pmi[term] = TopkHeap(top)
		for i in range(len(terms)):
			for j in range(i, len(terms)):
				# PMI(t1, t2) = log(p(t1,t2)/(p(t1)p(t2)))
				pmi = math.log(self.inverted_index.concurrence(term[i], term[j]) \
					/(self.inverted_index.get_word_appear(term[i]) \
						* self.inverted_index.get_word_appear(term[j])),  2)
				self.term_pmi[terms[i]].push(PMIElement(terms[j], pmi))
				self.term_pmi[terms[j]].push(PMIElement(terms[i], pmi))

	def get_top_pmi(self, term):
		return self.term_pmi[term]
