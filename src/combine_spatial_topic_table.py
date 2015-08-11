__author__ = 'koitaroh'

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# combine_spatial_topic_table
# Last Update: 2015-08-10
# @author: Satoshi Miyazawa
# koitaroh@gmail.com

import itertools, operator, os, datetime, csv, pandas
import numpy as np

def combine(doctopic, unit_names):
    result = np.concatenate((unit_names.T, doctopic), axis=1)
    return result


if __name__ == '__main__':
    # doctopic = np.genfromtxt("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doctopic_twitter_20150709_13.csv", delimiter=',')
    # unit_names = np.genfromtxt("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/docnames_twitter_20150709_13.csv", delimiter=',', dtype=None)

    # test values
    doctopic = np.array([[1, 2], [3, 4]])
    doctopic2 = np.array([[0.03676471,  0.03676471,  0.06617647,  0.03676471, 0.03676471,
                         0.03676471,  0.05147059,  0.08088235,  0.06617647,  0.03676471,
                         0.03676471,  0.08088235,  0.05147059,  0.03676471,  0.08088235,
                         0.03676471,  0.05147059,  0.05147059,  0.03676471,  0.05147059],
                         [0.04545455,  0.04545455,  0.04545455,  0.04545455,  0.04545455,
                          0.04545455,  0.04545455,  0.04545455,  0.04545455,  0.04545455,
                          0.04545455,  0.04545455,  0.06363636,  0.04545455,  0.06363636,
                          0.04545455,  0.08181818,  0.06363636,  0.04545455,  0.04545455]])

    unit_names = np.array([[1,2]])
    unit_names2 = np.array([[2015031714, 2015031715]])
    print(unit_names2)
    result = combine(doctopic2, unit_names2)
    print(result)
    np.savetxt("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/spatialtopic_20150811.csv", result, delimiter=",")
