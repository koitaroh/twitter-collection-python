#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lda_twitter.py
# Last Update: 2015-06-13
# @author: Satoshi Miyazawa
# koitaroh@gmail.com
# Objective: Run LDA
# per location
# per hour


import csv, codecs, itertools, operator, os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

filename = '/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/tweet_df_20150318_20150324.csv'


def grouper(n, iterable, fillvalue=None):
    # "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

doctopic_triples = []
mallet_docnames = []



def main(filename):
  

if __name__ == '__main__':
    clusters = main(filename)
    # f = codecs.open('%s.txt' % filename, 'w', 'utf-8')
    # for i,tweets in enumerate(clusters):
    #     for tweet in tweets:
    #         f.write('%d: %s\n' % (i, tweet.replace('/n', '')))
    # f.close()