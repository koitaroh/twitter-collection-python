#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lda_analyze_twitter.py
# Last Update: 2015-06-13
# @author: Satoshi Miyazawa
# koitaroh@gmail.com
# Objective: Run LDA
# per location
# per hour


import itertools, operator, os
import numpy as np

CORPUS_PATH = os.path.join('/Users/koitaroh/Documents/Data/Tweet/', 'ClassifiedTweet_20150709')
filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])


def grouper(n, iterable, fillvalue=None):
    # "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

doctopic_triples = []
mallet_docnames = []

with open("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doc-topics-tweet-20150709.txt", encoding="utf-8") as f:
    f.readline()  # read one line in order to skip the header
    for line in f:
        docnum, docname, *values = line.rstrip().split('\t')
        mallet_docnames.append(docname)
        for topic, share in grouper(2, values):
            triple = (docname, int(topic), float(share))
            doctopic_triples.append(triple)

# sort the triples
# triple is (docname, topicnum, share) so sort(key=operator.itemgetter(0,1))
# sorts on (docname, topicnum) which is what we want

doctopic_triples = sorted(doctopic_triples, key=operator.itemgetter(0,1))
mallet_docnames = sorted(mallet_docnames)
num_docs = len(mallet_docnames)
num_topics = len(doctopic_triples) // len(mallet_docnames)
doctopic = np.zeros((num_docs, num_topics))

for triple in doctopic_triples:
    docname, topic, share = triple
    row_num = mallet_docnames.index(docname)
    doctopic[row_num, topic] = share



def main(filename):


if __name__ == '__main__':
    clusters = main(filename)
    # f = codecs.open('%s.txt' % filename, 'w', 'utf-8')
    # for i,tweets in enumerate(clusters):
    #     for tweet in tweets:
    #         f.write('%d: %s\n' % (i, tweet.replace('/n', '')))
    # f.close()