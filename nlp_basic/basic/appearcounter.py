#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a tool to count words appear
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from tfidf import TfIdf

class AppearCount(TfIdf):

	def init_file_count(self):
		self.word_count = {}
		self.word_doc_count = {}

	def count_file(self, _input):
		counted_words = set()
		words = [word for word in self.get_tokens(_input) if word in self.term_num_docs]
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
		fw = open(filename, 'w')
		for word in self.term_num_docs:
			if word not in word_doc_count:
				self.word_doc_count[word] = 0
		sorted_terms = sorted(self.word_doc_count.items(), key=itemgetter(1))
		for word, doc_count in sorted_terms:
			fw.write(word + "\t" + str(doc_count) + '\t' + str(self.word_count[word]) + '\n')
		fw.close()

	def get_term_appear_count(self, term):
		try:
			return self.word_count[term]
		except:
			return 0

	def get_term_appear_docs(self, term):
		try:
			return self.word_doc_count[term]
		except:
			return 0