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


class TopkHeap(object):

	'''Heap save the top k element

	Use the heapq in python.

	Attributes:
		k : top k
		data: a list contain the top k data
	'''
	
	def __init__(self, k = 50):
	    self.k = k
	    self.data = []
	
	def push(self, elem):
		'''Push new elem to heap
		
		Args:
			elem ： the elem to add
		'''
		if len(self.data) < self.k:
			heapq.heappush(self.data, elem)
		else:
			topk_small = self.data[0]
			if elem > topk_small:
				heapq.heapreplace(self.data, elem) 
	
	def topK(self):
		'''Get top k elements
		
		Returns:
			a list of top k
		'''
		return sorted(self.data)[::-1]


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
		inf = -float('inf')
		terms = self.iindex.get_terms()
		for term in terms:
			self.term_pmi[term] = TopkHeap(self.top)
		for i in range(len(terms)-1):
			for j in range(i+1, len(terms)):
				# PMI(t1, t2) = log(p(t1,t2)/(p(t1)p(t2)))
				to_log = self.iindex.concurrence(terms[i], terms[j]) \
					/(self.iindex.get_word_appear(terms[i]) \
						* self.iindex.get_word_appear(terms[j]))
				if to_log == 0:
					pmi = inf
				else:
					pmi = math.log(to_log,  2)
				self.term_pmi[terms[i]].push(PMIElement(terms[j], pmi))
				self.term_pmi[terms[j]].push(PMIElement(terms[i], pmi))

	def get_top_pmi(self, term):
		'''Get top pmi elements of given term.

		Args:
			term : the given term to get top pmi elements

		Returns:
			A list object of PMIElement
		'''
		return self.term_pmi[term].topK()
