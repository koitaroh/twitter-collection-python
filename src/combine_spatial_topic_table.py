__author__ = 'koitaroh'

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# combine_spatial_topic_table
# Last Update: 2015-08-17
# @author: Satoshi Miyazawa
# koitaroh@gmail.com

import itertools, operator, os, datetime, csv
import numpy as np
import pandas as pd

def combine(doctopic, unit_names):
    sdoctopic = pd.concat([unit_names, doctopic], axis=1)
    return sdoctopic

if __name__ == '__main__':
    doctopic = pd.read_csv("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/doctopic_twitter_20150709_21.csv", names = ['topic0','topic1','topic2','topic3','topic4','topic5','topic6','topic7','topic8','topic9','topic10','topic11','topic12','topic13','topic14','topic15','topic16','topic17','topic18','topic19'])
    unit_names = pd.read_csv("/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/docnames_twitter_20150709_21.csv", names = ['sid'])
    sdoctopic = combine(doctopic, unit_names)
    sdoctopic.to_csv('/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/sdoctopic_twitter_20150709_21.csv', encoding='utf-8')