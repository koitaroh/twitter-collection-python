# twitter-collection-python
[![Build Status](https://travis-ci.org/koitaroh/GeoTweetCollector.svg?branch=master)](https://travis-ci.org/koitaroh/GeoTweetCollector)
=========

Collect geotagged tweets using Twitter Streaming API.

### src

| file name     | Description                    |
| ------------- | ------------------------------ |
| GeoTweetCollector.py | collect geotagged tweets |
| GeoTweetCollector_ec2.py | for launching on EC2 |
| GeoTweetCollector_Phangan.py | test app with MongoDB and SearchAPI |

### important note:
In streaming.py:

line 161 to

`self._buffer += self._stream.read(read_len).decode('UTF-8', 'ignore')`

and line 171 to

`self._buffer += self._stream.read(self._chunk_size).decode('UTF-8', 'ignore')`

and then reinstalled via python3 setup.py install on my local copy of tweepy.

### Requirements:
* Python 3.4 or later
* tweepy
* MySQL
* config.cfg

You'll need a configuration file with twitter API authentication and MySQL connection information.
As specified on line 18, make a configuration file "config.cfg" in parent directory.
It's a text file. in it, write your twitter API keys and MySQL
connection file like below (replace * with your keys).

```
[twitter]
consumer_key = ****
consumer_secret = ****
access_token_key = ****
access_token_secret = ****

[local_db]
host = ****
user = ****
passwd = ****
db_name = ****
```