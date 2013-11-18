#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 
# This is a simple class related Tf-idf library.  
# The key idea is to find the top term in one class.
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

import math
import re
from operator import itemgetter
from topkheap import TopkHeap

class ClassTfIdf:

  '''Compute class realted tf-idf to find each class's keywords
  '''

  def __init__(self, class_num, corpus_filename = None, 
    cdf_filename = None, stopword_filename = None):
    '''Initialize the idf dictionary.  
    
    If a corpus file is supplied, reads the term appeared dictionary from it, in the
    format of:
      list of class total documents, splited by \t
      term: list of count of class realted documents containing the term splited by \t

    If a cdf file is supplied, reads the cdf dictionary from it, in the  
    format of:
      list of class total document, splited by \t
      term: list of class's cdf

    If a stopword file is specified, reads the stopword list from it, in
    the format of one stopword per line.

    Args:
      class_num: number of classes
      corpus_filename: the term-appeared file name
      cdf_filename: the tern-cdf file name
      stopword_filename: file with one stopword in one line
    '''
    self.class_num = class_num
    self.num_docs = [0] * class_num
    self.term_num_docs = {}     # term : [num_docs_containing_term]
    self.term_cdf = {}          # term : [class tf * class idf]
    self.stopwords = []

    if corpus_filename:
      self._load_corpus_file(corpus_filename)

    if cdf_filename:
      self._load_cdf_file(cdf_filename)

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = [line.strip() for line in stopword_file]

  def _load_corpus_file(self, corpus_filename):
    with open(corpus_filename, "r") as corpus_file:
      # Load number of documents.
      line = corpus_file.readline()
      self.num_docs = map(int, line.strip().split("\t"))

      # Reads "term:frequency" from each subsequent line in the file.
      for line in corpus_file:
        tokens = line.rpartition(":")
        term = tokens[0].strip()
        frequencys = map(int, tokens[2].strip().split("\t"))
        self.term_num_docs[term] = frequencys 

  def _load_cdf_file(self, cdf_filename):
    with open(cdf_filename, 'r') as cdf_file:
      # Load number of documents.
      line = cdf_file.readline()
      self.num_docs = map(int, line.strip().split("\t"))

      for line in cdf_file:
        tokens = line.rpartition(":")
        term = tokens[0].strip()
        cdfs = map(float, tokens[2].strip().split("\t"))
        self.term_cdf[term] = cdfs

  def get_tokens(self, str):
    return str.strip().split()

  def add_input_document(self, _class, input):
    if _class >= self.class_num:
      raise IndexError

    self.num_docs[_class] += 1
    words = set(self.get_tokens(input))
    for word in words:
      if word in self.term_num_docs:
        self.term_num_docs[word][_class] += 1
      else:
        self.term_num_docs[word] = [0] * self.class_num
        self.term_num_docs[word][_class] = 1

  def save_corpus_to_file(self, idf_filename):
    output_file = open(idf_filename, "w")
    output_file.write("\t".join(map(str, self.num_docs)) + "\n")
    for term, num_docs in self.term_num_docs.items():
      output_file.write(term + ":")
      for num_doc in num_docs:
        output_file.write(str(num_doc) + "\t")
      output_file.write("\n")
    output_file.close()
  
  def save_cdf_to_file(self, cdf_filename):
    output_file = open(cdf_filename, "w")
    output_file.write("\t".join(map(str, self.num_docs)) + "\n")
    for term, cdfs in self.term_cdf.items():
      output_file.write(term + ":")
      for cdf in cdfs:
        output_file.write(str(cdf) + "\t")
      output_file.write("\n")
    output_file.close()

  def get_num_docs(self, _class):
    return self.num_docs[_class]

  def compute_all_cdf(self):
    for term in self.term_num_docs:
      term_cla_p = [0.0] * self.class_num   # term's posibility of every class
      for i in range(self.class_num):
        term_cla_p[i] += self.term_num_docs[term][i] / self.get_num_docs(i)
      sum_p = sum(term_cla_p)
      term_cla_cdf = [0.0] * self.class_num # term's cdf of every class
      for i in range(self.class_num):
        term_cla_cdf[i] += self.term_num_docs[term][i] * math.log(1+((1+term_cla_p[i])/(1+sum_p-term_cla_p[i])))
      self.term_cdf[term] = term_cla_cdf

  def get_class_keywords(self, _class, top_k):
    heap = TopkHeap(top_k)
    for term in self.term_num_docs:
      heap.push((self.term_cdf[term][_class], term))
    return [item[1] for item in heap.topk()]
  
