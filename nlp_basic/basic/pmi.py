#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a simple PMI tool based on inverted_index
#
# Reference: http://en.wikipedia.org/wiki/Pointwise_mutual_information 
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from inverted_index import InvertedIndex
from topkheap import TopkHeap
import math

class PMIElement(object):

	'''Term's PMI element
	 
	With another term's value and pmi of this term and other term

	Attributes:
		t2 : another term
		pmi: pmi value of this term and t2
	'''

	def __init__(self, t2, pmi = 0):
		self.t2 = t2
		self.pmi = pmi

	def __gt__(self, element):
		# compare the pmi value
		if isinstance(element, PMIElement):
			return self.pmi > element.pmi
		raise TypeError

	def __eq__(self, other):  
		# must t2 and pmi equal
		if isinstance(other, PMIElement) and \
			other.t2 == self.t2 and other.pmi == self.pmi:
			return True
		return False

	def __str__(self):
		# t2:pmi
		return self.t2 + ":" + str(self.pmi)


class PMI(object):

	'''PMI compute for items based on InvertedIndex
	
	The library constructs an inverted index corpus from documents specified by reading from input files.
    Then compute all terms' pmi top k element and pmi score 

    Attributes:
    	iindex : the inverted index of given documents
    	top : means the k of top k elements while hold for one term
    	term_pmi : dictory of terms top pmi elements "term : list of PMIElement"
	'''

	def __init__(self, inverted_index, top = 50):
		'''init all attributes'''
		self.iindex = inverted_index
		self.top = top
		self.term_pmi = {}

	def change_inverted_index(self, inverted_index):
		'''change instance's iindex'''
		self.inverted_index = inverted_index

	def build(self):
		'''compute all terms' top pmi elements

		All terms computed is from iindex's get_terms method.
		'''
		
		terms = self.iindex.get_terms()
		for term in terms:
			self.term_pmi[term] = TopkHeap(self.top)
		for i in range(len(terms)-1):
			for j in range(i+1, len(terms)):
				pmi = self.compute_pmi(terms[i], terms[j])
				self.term_pmi[terms[i]].push(PMIElement(terms[j], pmi))
				self.term_pmi[terms[j]].push(PMIElement(terms[i], pmi))

	def compute_pmi(self, t1 , t2):
		# PMI(t1, t2) = log(p(t1,t2)/(p(t1)p(t2)))
		#             = concurrent * N / (xapp * yapp)
		to_log = self.iindex.concurrence(t1, t2) * self.iindex.get_num_docs() \
			/(self.iindex.get_word_appear(t1) \
			* self.iindex.get_word_appear(t2))
		if to_log == 0:
			return -float('inf')
		else:
			return math.log(to_log,  2)

	def get_top_pmi(self, term):
		'''Get top pmi elements of given term.

		Args:
			term : the given term to get top pmi elements

		Returns:
			A list object of PMIElement
		'''
		return self.term_pmi[term].topk()
