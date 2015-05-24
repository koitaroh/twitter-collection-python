#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*- 

# general_text_stats.py
# Last Update: 2015-05-14
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Objective: Run general text statistics on tweet database
# per user
# per location
# per time
#
# calculate number of unique users
# 	can be done in SQL
# calculate number of tweets
#
# compose tf-idf

import csv, codecs
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

filename = '../data/tweet_table_20150317140245.csv'

corpus = []

def get_tweets_from_csv(filename):
    ret = csv.reader(open(filename, encoding="utf-8"))
    # row 9 is words.
    tweets = [r[9] for r in ret]
    tweets2 = []
    for tweet in tweets[:]:
        tweet2 = tweet.replace(',', ' ')
        # print(tweet)
        print(tweet2)
        tweets2.append(tweet2)
        # if u'@' in tweet2:
        #     tweets.remove(tweet)
        # if len(tweet) <= 3:
        #     tweets.remove(tweet)
    # print(tweets2)
    return tweets2


# User's bag of data
# Location's bag of data

# def analyzer(text):
#     ret1 = []
#     ret1.append(text.split(','))
#     return ret1
#
def main(filename):
    # load tweets
    tweets = get_tweets_from_csv(filename)
    # test corpus
    corpus = [
        'This, is, the, first, document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]

    vectorizer = TfidfVectorizer(min_df=1)
    # vectorizer = CountVectorizer(min_df=1)
    # This is using the word analyzer. It excludes one-character-words.
    X = vectorizer.fit_transform(tweets)
    vocab = vectorizer.get_feature_names()
    print(X)
    print(vocab)
    print(type(X))
    # convert them to regular numpy array
    X = X.toarray()
    vocab = np.array(vocab)

    print(tweets[2])
    print(tweets[3])
    print(X[2, vocab == 'なう'])
    print(X[3, vocab == 'なう'])
    print(X[1, vocab == '松山'])
    print(X[2, vocab == '松山'])

#     # feature extraction
#     vectorizer = TfidfVectorizer(analyzer=analyzer, max_df=MAX_DF)
#     vectorizer.max_features = MAX_FEATURES
#     X = vectorizer.fit_transform(tweets)
#
#     # dimensionality reduction by LSA
#     lsa = TruncatedSVD(LSA_DIM)
#     X = lsa.fit_transform(X)
#     X = Normalizer(copy=False).fit_transform(X)
#
#     # clustering by KMeans
#     if MINIBATCH:
#         km = MiniBatchKMeans(n_clusters=NUM_CLUSTERS, init='k-means++', batch_size=1000, n_init=10, max_no_improvement=10, verbose=True)
#     else:
#         km = KMeans(n_clusters=NUM_CLUSTERS, init='k-means++', n_init=1, verbose=True)
#     km.fit(X)
#     labels = km.labels_
#
#     transformed = km.transform(X)
#     dists = np.zeros(labels.shape)
#     for i in range(len(labels)):
#         dists[i] = transformed[i, labels[i]]
#
#     # sort by distance
#     clusters = []
#     for i in range(NUM_CLUSTERS):
#         cluster = []
#         ii = np.where(labels==i)[0]
#         dd = dists[ii]
#         di = np.vstack([dd,ii]).transpose().tolist()
#         di.sort()
#         for d, j in di:
#             cluster.append(tweets[int(j)])
#         clusters.append(cluster)
#
#     return clusters
#
#
if __name__ == '__main__':
    clusters = main(filename)
    # f = codecs.open('%s.txt' % filename, 'w', 'utf-8')
    # for i,tweets in enumerate(clusters):
    #     for tweet in tweets:
    #         f.write('%d: %s\n' % (i, tweet.replace('/n', '')))
    # f.close()