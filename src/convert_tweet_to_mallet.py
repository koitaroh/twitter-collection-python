__author__ = 'koitaroh'

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# run_general_text_stats.py
# Last Update: 2015-07-06
# Author: Satoshi Miyazawa
# koitaroh@gmail.com

import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from datetime import datetime, date, time
import numpy as np
import pandas as pd

def convert_tweet_to_mallet(filename):
    tweet_df = pd.read_csv(filename)

if __name__ == '__main__':
    # If dataframe is already created
    filename = '/Users/koitaroh/Documents/GitHub/GeoTweetCollector/data/tweet_df_20150317142835.csv'
