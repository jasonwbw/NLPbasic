#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 
# Copyright 2010  Niniane Wang (niniane@gmail.com)
# Reviewed by Alex Mendes da Costa.
#
# Edit by Jason wu (Jasonwbw@yahoo.com)
# 
# This is a simple Tf-idf library.  The algorithm is described in
#   http://en.wikipedia.org/wiki/Tf-idf

__author__ = "Niniane Wang"
__email__ = "niniane at gmail dot com"

import math
import re
from operator import itemgetter

class TfIdf:

  '''Tf-idf class implementing http://en.wikipedia.org/wiki/Tf-idf.
  
     The library constructs an IDF corpus and stopword list either from
     documents specified by the client, or by reading from input files.  It
     computes IDF for a specified term based on the corpus, or generates
     keywords ordered by tf-idf for a specified document.
  '''

  def __init__(self, corpus_filename = None, stopword_filename = None,
               DEFAULT_IDF = 1.5):
    '''Initialize the idf dictionary.  
    
    If a corpus file is supplied, reads the idf dictionary from it, in the
    format of:
      # of total documents
      term: # of documents containing the term

    If a stopword file is specified, reads the stopword list from it, in
    the format of one stopword per line.

    The DEFAULT_IDF value is returned when a query term is not found in the
    idf corpus.

    Args:
      corpus_filename : old idf file, format: save by this class
      stopword_filename : stopword file, format: one stopword one line
      DEFAULT_IDF : default idf for the term that have not appeared
    '''
    self.num_docs = 0
    self.term_num_docs = {}     # term : num_docs_containing_term
    self.stopwords = []
    self.idf_default = DEFAULT_IDF

    if corpus_filename:
      corpus_file = open(corpus_filename, "r")

      # Load number of documents.
      line = corpus_file.readline()
      self.num_docs = int(line.strip())

      # Reads "term:frequency" from each subsequent line in the file.
      for line in corpus_file:
        term, fstr = line.strip().split("\t")
        frequency = int(fstr)
        self.term_num_docs[term] = frequency

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = [line.strip() for line in stopword_file]

  def get_tokens(self, _str, token = None):
    '''Break a string into tokens, preserving URL tags as an entire token.

    This implementation does not preserve case.  
    Clients may wish to override this behavior with their own tokenization.

    Args:
      _str : the str to split by token
      token : token for split, default is space
    '''
    if token:
      return _str.strip().split(token)
    return _str.strip().split(token)

  def add_input_document(self, _input, token = None, filter_num = True):
    '''Add terms in the specified document to the idf dictionary.

    Args:
      _input : the input text for term split by token
      token : token to split term
      filter_num : whether filter all numbers
    '''
    self.num_docs += 1
    if filter_num:
      p = re.compile(r'\d*', re.L)
    words = set(self.get_tokens(_input, token = token))
    for word in words:
      if filter_num:
        word = p.sub("", word)
      if word in self.term_num_docs:
        self.term_num_docs[word] += 1
      else:
        self.term_num_docs[word] = 1

  def save_corpus_to_file(self, idf_filename, stopword_filename, stopword_less_k = 10):
    '''Save the idf dictionary and stopword list to the specified file.

    Args:
      idf_filename : new idf file name to save all corpus.(contain stopwords)
      stopword_filename : new stopword file to save stopword words
      stopword_less_k : if term appear doc number less than this, it will save to stopwords
    '''
    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1), reverse=True)
    output_file = open(idf_filename, "w")
    stopword_file = open(stopword_filename, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in sorted_terms:
      output_file.write(term + "\t" + str(num_docs) + "\n")
      if num_docs < stopword_less_k:
        stopword_file.write(term + "\n")
    output_file.close()
    stopword_file.close()

  def save_corpus_to_without_stop(self, idf_filename, stopword_file, stopword_less_k = 0, filters = [], keepwords = []):
    '''Just save the idf dictionary to the specified file without stopwords list and filtered by filters.
    And save all other words into stopword_file

    Args:
      idf_filename : new idf file name to save all corpus.
      stopword_filename : new stopword file to save stopword words
      stopword_less_k : if term appear doc number less than this, it will save to stopwords
      filters : lambda functions to filter terms if it return true
      keepwords: just for these words that appear less than stopword_less_k
    '''
    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1), reverse=True)
    output_file = open(idf_filename, "w")
    stopword_file = open(stopword_file, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in sorted_terms:
      if num_docs < stopword_less_k and term not in keepwords:
        stopword_file.write(term + "\n")
        continue
      if term in self.stopwords:
        stopword_file.write(term + "\n")
        continue

      filtered = False
      for _filter in filters:
        if not filtered and _filter(term.strip()):
          filtered = True

      if not filtered:
        output_file.write(term + "\t" + str(num_docs) + "\n")
      else:
        stopword_file.write(term + "\n")

    output_file.close()
    stopword_file.close()

  def get_num_docs(self):
    '''Get total doc number

    Returns:
      Return the total number of documents in the IDF corpus.
    '''
    return self.num_docs

  def get_num_words(self):
    '''Get total term number

    Returns:
      Return the total number of term in the IDF corpus.
    '''
    return len(self.term_num_docs)

  def get_idf(self, term):
    '''Retrieve the IDF for the specified term. 
    
    This is computed by taking the logarithm of ((number of documents in corpus) divided by (number of documents containing this term) ).

    Args:
      term : term to get idf

    Returns:
      Return the idf value.
    '''
    if term in self.stopwords:
      return 0

    if not term in self.term_num_docs:
      return self.idf_default

    return math.log(float(1 + self.get_num_docs()) / 
      (1 + self.term_num_docs[term]))
  
  def get_doc_keywords(self, curr_doc):
    """Retrieve terms and corresponding tf-idf for the specified document.

    Args:
      curr_doc : computed given doc

    Returns:
      The returned terms are ordered by decreasing tf-idf.
    """
    tfidf = {}
    tokens = self.get_tokens(curr_doc)
    tokens_set = set(tokens)
    for word in tokens_set:
      # The definition of TF specifies the denominator as the count of terms
      # within the document, but for short documents, I've found heuristically
      # that sometimes len(tokens_set) yields more intuitive results.
      mytf = float(tokens.count(word)) / len(tokens)
      myidf = self.get_idf(word)
      tfidf[word] = mytf * myidf

    return sorted(tfidf.items(), key=itemgetter(1), reverse=True)
