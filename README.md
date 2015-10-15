# GeoTweetCollector
[![Build Status](https://travis-ci.org/koitaroh/GeoTweetCollector.svg?branch=master)](https://travis-ci.org/koitaroh/GeoTweetCollector)
=========

Collect geotagged tweets using Twitter Streaming API.

### src

| file name     | Description                    |
| ------------- | ------------------------------ |
| GeoTweetCollector.py | collect geotagged tweets |
| GeoTweetCollector_dev.py | In development |
| GeoTweetCollector_dev_3.py | In development for Python 3 compatibility |

### important note:
In streaming.py:

line 161 to
`self._buffer += self._stream.read(read_len).decode('UTF-8', 'ignore')`
and line 171 to
`self._buffer += self._stream.read(self._chunk_size).decode('UTF-8', 'ignore')`
and then reinstalled via python3 setup.py install on my local copy of tweepy.