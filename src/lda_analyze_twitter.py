#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lda_analyze_twitter.py
# Last Update: 2015-06-13
# @author: Satoshi Miyazawa
# koitaroh@gmail.com
# Objective: Run LDA
# per location
# per hour


import itertools, operator, os, datetime, csv
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

print("Importing file at:"+ str(datetime.datetime.now()) )

# CORPUS_PATH = os.path.join('../data/', 'ClassifiedTweet_sample')
CORPUS_PATH = os.path.join('/Users/koitaroh/Documents/Data/Tweet/', 'ClassifiedTweet_20150709')
filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])


def grouper(n, iterable, fillvalue=None):
    # "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

doctopic_triples = []
mallet_docnames = []

print("Appending triples at:"+ str(datetime.datetime.now()))

# with open("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doc-topics-tweet.txt", encoding="utf-8") as f:
with open("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doc-topics-tweet-20150709.txt", encoding="utf-8") as f:
    f.readline()  # read one line in order to skip the header
    for line in f:
        docnum, docname, *values = line.rstrip().split('\t')
        mallet_docnames.append(docname)
        for topic, share in grouper(2, values):
            triple = (docname, int(topic), float(share))
            doctopic_triples.append(triple)

print("Sorting the triples at:"+ str(datetime.datetime.now()))
# sort the triples
# triple is (docname, topicnum, share) so sort(key=operator.itemgetter(0,1))
# sorts on (docname, topicnum) which is what we want

doctopic_triples = sorted(doctopic_triples, key=operator.itemgetter(0,1))
mallet_docnames = sorted(mallet_docnames)
num_docs = len(mallet_docnames)
num_topics = len(doctopic_triples) // len(mallet_docnames)
doctopic = np.zeros((num_docs, num_topics))

print("Creating doctopic matrix at:"+ str(datetime.datetime.now()))

i = 0
for triple in doctopic_triples:
    docname, topic, share = triple
    j = i//num_topics
    # row_num = mallet_docnames.index(docname)
    doctopic[j, topic] = share
    i += 1
np.savetxt("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doctopic_twitter_20150709.csv", doctopic, delimiter=",")

writer = open("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/docnames_twitter_20150709.csv", 'w', newline='', encoding="utf-8")
for row in mallet_docnames:
    basename = os.path.basename(row)
    name, ext = os.path.splitext(basename)
    writer.write(name+'\n')
writer.close()

# doctopic =  open('/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doctopic_twitter_20150730.csv', encoding="utf-8")

# print("Creating analysis unit 13 at:"+ str(datetime.datetime.now()))
# unit_names = []
# for fn in filenames:
#     basename = os.path.basename(fn)
#     name, ext = os.path.splitext(basename)
#     name = name.rstrip('0123456789')
#     name = name.rstrip('-')
#     name = name.rstrip('_')
#     name = name.rstrip('0123456789')
#     name = name.rstrip('-')
#     name = name.rstrip('_')
#     unit_names.append(name)
#
# print("Grouping doctopic matrix for 13 at:"+ str(datetime.datetime.now()))
# unit_names = np.asarray(unit_names)
# doctopic_orig = doctopic.copy()
# num_groups = len(set(unit_names))
# doctopic_grouped = np.zeros((num_groups, num_topics))
# for i, name in enumerate(sorted(set(unit_names))):
#     doctopic_grouped[i, :] = np.mean(doctopic[unit_names == name, :], axis=0)
# doctopic = doctopic_grouped
#
# print("Saving doctopic_twitter for scenario 13 at:"+ str(datetime.datetime.now()))
# np.savetxt("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doctopic_twitter_20150709_13.csv", doctopic, delimiter=",")
# writer2 = open("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/docnames_twitter_20150709_13.csv", 'w', newline='', encoding="utf-8")
# unit_names = sorted(set(unit_names))
# for row in unit_names:
#     writer2.write(row+'\n')
# writer2.close()

print("Creating analysis unit 21 at:"+ str(datetime.datetime.now()))
unit_names = []
for fn in filenames:
    basename = os.path.basename(fn)
    name, ext = os.path.splitext(basename)
    name = name.lstrip('0123456789')
    name = name.lstrip('_')
    name = name.replace('-', '0')
    unit_names.append(name)

print("Grouping doctopic matrix for 21 at:"+ str(datetime.datetime.now()))
unit_names = np.asarray(unit_names)
num_groups = len(set(unit_names))
doctopic_grouped = np.zeros((num_groups, num_topics))
for i, name in enumerate(sorted(set(unit_names))):
    doctopic_grouped[i, :] = np.mean(doctopic[unit_names == name, :], axis=0)
doctopic = doctopic_grouped

print("Saving doctopic_twitter for scenario 21 at:"+ str(datetime.datetime.now()))
np.savetxt("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doctopic_twitter_20150709_21.csv", doctopic, delimiter=",")
writer2 = open("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/docnames_twitter_20150709_21.csv", 'w', newline='', encoding="utf-8")
unit_names = sorted(set(unit_names))
for row in unit_names:
    writer2.write(row+'\n')
writer2.close()

# print("Running Vectorizer at:"+ str(datetime.datetime.now()))
# # CORPUS_PATH_UNSPLIT = os.path.join('../data/', 'ClassifiedTweet_sample')
# CORPUS_PATH_UNSPLIT = os.path.join('/Users/koitaroh/Documents/Data/Tweet/', 'ClassifiedTweet_20150709')
# filenames = [os.path.join(CORPUS_PATH_UNSPLIT, fn) for fn in sorted(os.listdir(CORPUS_PATH_UNSPLIT))]
# vectorizer = CountVectorizer(input='filename')
# dtm = vectorizer.fit_transform(filenames)  # a sparse matrix
# novels = sorted(set(unit_names))
#
# print("Listing top topics in each unit:"+ str(datetime.datetime.now()))
# print("Top topics in...")
# for i in range(len(doctopic)):
#     top_topics = np.argsort(doctopic[i,:])[::-1][0:3]
#     top_topics_str = ' '.join(str(t) for t in top_topics)
#     print("{}: {}".format(novels[i], top_topics_str))
# # with open('/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/topic-keys-tweet.txt', encoding="utf-8") as input:
# with open('/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/topic-keys-tweet-20150714.txt', encoding="utf-8") as input:
#     topic_keys_lines = input.readlines()
# topic_words = []
# for line in topic_keys_lines:
#     _, _, words = line.split('\t')  # tab-separated
#     words = words.rstrip().split(' ')  # remove the trailing '\n'
#     topic_words.append(words)
# N_WORDS_DISPLAY = 10
# for t in range(len(topic_words)):
#     print("Topic {}: {}".format(t, ' '.join(topic_words[t][:N_WORDS_DISPLAY])))

# def main(filename):
#
#
# if __name__ == '__main__':
#     clusters = main(filename)
    # f = codecs.open('%s.txt' % filename, 'w', 'utf-8')
    # for i,tweets in enumerate(clusters):
    #     for tweet in tweets:
    #         f.write('%d: %s\n' % (i, tweet.replace('/n', '')))
    # f.close()