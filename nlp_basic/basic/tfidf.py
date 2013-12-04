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

  """Tf-idf class implementing http://en.wikipedia.org/wiki/Tf-idf.
  
     The library constructs an IDF corpus and stopword list either from
     documents specified by the client, or by reading from input files.  It
     computes IDF for a specified term based on the corpus, or generates
     keywords ordered by tf-idf for a specified document.
  """

  def __init__(self, corpus_filename = None, stopword_filename = None,
               DEFAULT_IDF = 1.5):
    """Initialize the idf dictionary.  
    
       If a corpus file is supplied, reads the idf dictionary from it, in the
       format of:
         # of total documents
         term: # of documents containing the term

       If a stopword file is specified, reads the stopword list from it, in
       the format of one stopword per line.

       The DEFAULT_IDF value is returned when a query term is not found in the
       idf corpus.
    """
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

  def get_tokens(self, _str):
    """Break a string into tokens, preserving URL tags as an entire token.

       This implementation does not preserve case.  
       Clients may wish to override this behavior with their own tokenization.
    """
    #return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())
    return _str.strip().split()

  def add_input_document(self, _input):
    """Add terms in the specified document to the idf dictionary."""
    self.num_docs += 1
    words = set(self.get_tokens(_input))
    for word in words:
      if word in self.term_num_docs:
        self.term_num_docs[word] += 1
      else:
        self.term_num_docs[word] = 1

  def save_corpus_to_file(self, idf_filename, stopword_filename):
    """Save the idf dictionary and stopword list to the specified file."""
    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1), reverse=True)
    output_file = open(idf_filename, "w")
    stopword_file = open(stopword_filename, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in sorted_terms:
      output_file.write(term + "\t" + str(num_docs) + "\n")
      if num_docs < 10:
        stopword_file.write(term + "\n")
    output_file.close()
    stopword_file.close()

  def save_corpus_to_without_stop(self, idf_filename, stopword_file, appear_num, filters, keepwords = []):
    """Save the idf dictionary and stopword list to the specified file.

    keepwords: just for these words that appear less than appear_num
    """
    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1), reverse=True)
    output_file = open(idf_filename, "w")
    stopword_file = open(stopword_file, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in sorted_terms:
      if num_docs < appear_num and term not in keepwords:
        stopword_file.write(term + "\n")
        continue
      if term in self.stopwords:
        stopword_file.write(term + "\n")
        continue

      filtered = False
      for _filter in filters:
        if not filtered and _filter(term.strip()) == '':
          filtered = True

      if not filtered:
        output_file.write(term + "\t" + str(num_docs) + "\n")
      else:
        stopword_file.write(term + "\n")

    output_file.close()
    stopword_file.close()

  def get_num_docs(self):
    """Return the total number of documents in the IDF corpus."""
    return self.num_docs

  def get_idf(self, term):
    """Retrieve the IDF for the specified term. 
    
       This is computed by taking the logarithm of ( 
       (number of documents in corpus) divided by (number of documents
        containing this term) ).
     """
    if term in self.stopwords:
      return 0

    if not term in self.term_num_docs:
      return self.idf_default

    return math.log(float(1 + self.get_num_docs()) / 
      (1 + self.term_num_docs[term]))

  def get_idf_file(self, idf_filename):
    """Save the idf dictionary and stopword list to the specified file."""
    output_file = open(idf_filename, "w")

    for term, num_docs in self.term_num_docs.items():
      output_file.write(term + "\t" + str(self.get_idf(term)) + "\n")
  
  def get_doc_keywords(self, curr_doc):
    """Retrieve terms and corresponding tf-idf for the specified document.

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
