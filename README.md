# twitter-collection-python
[![Build Status](https://travis-ci.org/koitaroh/twitter-collection-python.svg?branch=master)](https://travis-ci.org/koitaroh/twitter-collection-python)
=========

Collect tweets using Twitter API and store in MySQL database.

### src

| file name     | Description                    |
| ------------- | ------------------------------ |
| dump_user_timeline.py | dump a user's timeline into csv |
| TweetCollector.py | collect geo-tagged tweets |
| TweetCollector_ec2.py | for launching on EC2 |


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

### Workflow
1. Prepare Python and MySQL environment.
2. Run TweetCollector.py and keep it running.