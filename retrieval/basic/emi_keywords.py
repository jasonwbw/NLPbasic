#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a simple Inverted Index library to pretreatment for Estimeated_MI compute
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from operator import itemgetter
from topkheap import TopkHeap
import math

class ClassInvertedIndex(object):

  '''Inverted Index class for docs

  The library constructs an inverted index corpus from documents specified by the client or reading from input files.
  It saves the document appear and handle some count for PMI or other algorithm.

  Attributes:
    num_docs: number of document computed
    stopwords: stopword list
    term_count: dictory of "term : appeared document count" this is a lazy loading dictory
    have_vocabulary: have vocabulary or not
    vocabulary: the given vocabulary
  '''   

  def __init__(self, vocabulary = None, stopword_filename = None):
    '''Initialize the index.

    If a stopword file is specified, reads the stopword list from it, in
    the format of one stopword per line.

    Args:
      vocabulary : to build inverted index just for term in this vocabulary
      stopword_filename: file with one stopword in one line
    '''
 
    self.num_docs = 0
    self.stopwords = []    
    self.term_count = {}  # word : {class : count}
    self.class_count = {} # class : count
    self.have_vocabulary = False

    if vocabulary:
      self.have_vocabulary = True
      self.vocabulary = set(vocabulary)

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = set([line.strip() for line in stopword_file])

  def get_tokens(self, _str):
    '''Break a string into tokens, preserving URL tags as an entire token.

    This implementation does not preserve case.  
    Clients may wish to override this behavior with their own tokenization.

    Args:
      _str: the string to split
    '''
    return _str.strip().split()
  
  def add_input_document(self, _input, _class):
    '''Add terms in the specified document to the inverted index.

    Args:
      _input: the input content
      _class: the class of intput content
    '''
    words = set(self.get_tokens(_input))
    for word in words:
      if self.have_vocabulary and word not in self.vocabulary:
        continue
      if word in self.stopwords:
        continue

      if word not in self.term_count:
        self.term_count[word] = {}
        self.term_count[word][_class] = 1
      try:
        self.term_count[word][_class] += 1
      except:
        self.term_count[word][_class] = 1
      try:
        self.class_count[_class] += 1
      except:
        self.class_count[_class] = 1
    self.num_docs += 1

  def get_num_docs(self):
    '''Return the total number of documents added.

    Returns:
      Total number of documents
    '''
    return self.num_docs

  def get_terms(self):
    '''Return the terms

    Returns:
      A list object of terms
    '''
    return self.term_count.keys()

  def get_classes(self):
    '''Return all classes name

    Returns:
      A list object for classes
    '''
    return self.class_count.keys()

  def get_word_appear(self, word, _class):
    try:
      return self.term_count[word][_class]
    except:
      return 0

  def get_class_count(self, _class):
    try:
      return self.class_count[_class]
    except:
      return 0

class EstimateMi(object):

  def __init__(self, ciindex):
    self.ciindex = ciindex

  def estimate_mi(self, _class, word):
    '''Return the estimate mi of class and word

    Args:
      _class: the _class the chek word
      word: the word to check

    Returns:
      estimate mi value
    '''
    A = self.ciindex.get_word_appear(word, _class)
    B = self.ciindex.get_num_docs() - A
    C = self.ciindex.get_class_count(_class) - A
    N = self.ciindex.get_num_docs()
    if A == 0 or A + C == 0 or A + B == 0:
      return 0.0
    # return math.log(float(A*N)/((A+C) * (A+B)))
    return float(A*N)/((A+C) * (A+B))

  def find_top_word(self, _class, topk = None):
    '''Find the keywords of given _class

    Args:
      _class: the _class the chek word
      topk: top k keywords to find, None means all words

    Returns:
      a list of topk term
    '''
    if topk:
      heap = TopkHeap(topk)
      for term in self.ciindex.get_terms():
        heap.push((self.estimate_mi(_class, term), term))
      return heap.topk()
    else:
      res = []
      for term in self.ciindex.get_terms():
        res.append((self.estimate_mi(_class, term), term))
      return sorted(res)[::-1]

