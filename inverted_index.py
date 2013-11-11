#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is a simple Inverted Index library to pretreatment for PMI compute or similar way
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from operator import itemgetter

class InvertedIndex(object):

  '''
  Inverted Index class for docs

    The library constructs an inverted index corpus from documents specified by the client or reading from input files.
    It saves the document appear and handle some count for PMI or other algorithm.
  '''   

  def __init__(self, stopword_filename = None):
    '''
    Initialize the index.

      If a stopword file is specified, reads the stopword list from it, in
      the format of one stopword per line.

    Attributes:
      stopword_filename: file with one stopword in one line
    '''
 
    self.num_docs = 0
    self.term_doc = {}     # term : [docnum]
    self.stopwords = []    # stopwords
    self.term_count = {}   # term appear doc count

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = [line.strip() for line in stopword_file]

  def get_tokens(self, _str):
    '''
    Break a string into tokens, preserving URL tags as an entire token.

      This implementation does not preserve case.  
      Clients may wish to override this behavior with their own tokenization.

    Attributes:
      _str: the string to split
    '''
    return _str.strip().split()
  
  def add_input_document(self, _input):
    '''
    Add terms in the specified document to the inverted index.

    Attributes:
      _input: the input content
    '''
    words = set(self.get_tokens(_input))
    for word in words:
      try:
        self.term_doc[word]
        self.term_doc[word].append(self.num_docs)
      except:
        self.term_doc[word] = [self.num_docs, ]
    self.num_docs += 1

  def save_corpus_to_file(self, index_filename):
    '''
    Save the inverted index to the specified file.
    
    Attributes:
      index_filename: the specified file
    '''
    output_file = open(index_filename, "w")
    
    output_file.write(str(self.num_docs) + "\n")
    for key, value in self.term_doc.items():
      output_file.write(key + "\t" + "\t".join([str(i) for i in value]) + "\n")
    output_file.close()
  
  def load_corpus_from_file(self, index_filename):
    '''
    Load corpus from index file,  this file must builded from this class by save_corpus_to_file method
    
    Attributes:
      index_filename: build by save_corpus_to_file
    '''
    self.term_doc = {}   
    self.term_count = {} 
    with open(index_filename) as fp:
      line = fp.readline()
      self.num_docs = int(line.strip())
      for line in fp:
        word, docs = line.split("\t", 1)
        self.term_doc[word] = map(int, docs.split("\t"))

  def get_num_docs(self):
    '''
    Return the total number of documents added.
    '''
    return self.num_docs
  
  def concurrence(self, w1, w2):
    '''
    Return the concurrence of w1 and w2 in one document
      add one for smoothness

    Attributes:
      w1: one word
      w2: another word
    '''
    count = 0.0
    try:
      for item in self.term_doc[w1]: 
        if item in self.term_doc[w2] : count += 1
    except:
      pass
    return count
  
  def get_word_appear(self, word):
    '''
    Return the count of the document word appeared.
      added one for smoothness

    Attributes:
      word: the check word
    '''
    # recorded in term_count
    base = 0.0
    try:
      return self.term_count[word]
    except:
      pass
    try:
      self.term_count[word] = base + len(self.term_doc[word])
      return self.term_count[word]
    except:
      return base

  def __iter__(self):
    '''
    Return the term : [docnum]
    '''
    for x in self.term_doc.items():
      yield x

  def get_terms(self):
    '''
    Return the terms
    '''
    return self.term_doc.keys()

