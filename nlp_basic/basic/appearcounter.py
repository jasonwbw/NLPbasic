#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a tool to count words appear
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from tfidf import TfIdf
from operator import itemgetter

class AppearCount(TfIdf):
	def __init__(self, corpus_filename = None, stopword_filename = None, DEFAULT_IDF = 1.5):
		TfIdf.__init__(self, corpus_filename = corpus_filename, \
			stopword_filename = stopword_filename, DEFAULT_IDF = DEFAULT_IDF)
		self.init_file_count()

	def init_file_count(self):
		'''Init the data structure to save the count
		'''
		self.word_count = {}
		self.word_doc_count = {}

	def count_file(self, _input, token = None):
		'''count the given file

		Args:
			_input : the input text for term split by token
			token : token to split term
		'''
		counted_words = set()
		words = [word for word in self.get_tokens(_input, token = token) if word in self.term_num_docs]
		for word in words:
			try:
				self.word_count[word] += 1
			except:
				self.word_count[word] = 1
			if word not in counted_words:
				try:
					self.word_doc_count[word] += 1
				except:
					self.word_doc_count[word] = 1
			counted_words.add(word)

	def get_count_result(self, filename):
		'''Write the count result to file

		Args:
			filename : file to save the result
		'''
		fw = open(filename, 'w')
		for word in self.term_num_docs:
			if word not in self.word_doc_count:
				self.word_doc_count[word] = 0
				self.word_count[word] = 0
		sorted_terms = sorted(self.word_doc_count.items(), key=itemgetter(1))
		for word, doc_count in sorted_terms:
			fw.write(str(doc_count) + "\t" + str(self.word_count[word]) + '\t' + word + '\n')
		fw.close()

	def get_term_appear_count(self, term):
		'''Get the appear time of given term

		Args:
			term : term to check the appear time

		Returns:
			appear count
		'''
		try:
			return self.word_count[term]
		except:
			return 0

	def get_term_appear_docs(self, term):
		'''Get the docs count where given term appeared

		Args:
			term : term to check the appear time

		Returns:
			doc count
		'''
		try:
			return self.word_doc_count[term]
		except:
			return 0

	def load_result_foranalyze(self, result_file):
		'''Load the result file and prepare for analyze

		Args:
			result_file : result file build by get_count_result method
		'''
		self.count_word = {}
		self.doc_count_word = {}
		with open(result_file, 'r') as fp:
			for line in fp:
				doc_count, count, word = line.strip().split("\t")
				self.word_count[word] = int(count)
				self.word_doc_count[word] = int(doc_count)
				try:
					self.count_word[int(count)] += 1
				except:
					self.count_word[int(count)] = 1
				try:
					self.doc_count_word[int(doc_count)] += 1
				except:
					self.doc_count_word[int(doc_count)] = 1

	def count_less_appear(self, less_than):
		'''Count word count that appeared count less than given threshold
		Must call after load_result_foranalyze

		Args:
			less_than : the threshold

		Returns:
			the count
		'''
		res = 0
		for i in range(less_than):
			if i in self.count_word:
				res += self.count_word[i]
		return res

	def doccount_less_appear(self, less_than):
		'''Count word count that appeared doc count less than given threshold
		Must call after load_result_foranalyze

		Args:
			less_than : the threshold

		Returns:
			the count
		'''
		res = 0
		for i in range(less_than):
			if i in self.doc_count_word:
				res += self.doc_count_word[i]
		return res

	def get_words_doccount_less_appear(self, less_than):
		'''Get word that doc it appeared in less than threshold

		Args:
			less_than : the threshold

		Returns:
			List of words that doc it appeared in less than threshold
		'''
		res = []
		for word, doc_count in self.word_doc_count.items():
			if doc_count < less_than:
				res.append(word)
		return res

	def get_words_less_appear(self, less_than):
		'''Get the word appear less than threshold

		Args:
			less_than : the threshold

		Returns:
			List of words that appeared in less than threshold
		'''
		res = []
		for word, count in self.word_count.items():
			if count < less_than:
				res.append(word)
		return res