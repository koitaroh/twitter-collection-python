# Last Update: 2015-11-15
# Python 3.5
# Requirements
# 1. Fill consumer_key, consumer_secret, access_key, and access_secret for Twitter API, or create config.cfg file with the keys (read README.md).
# 2. Replace the twitter user name at line 69.

import tweepy, csv, configparser, pytz

#Twitter API credentials
conf = configparser.ConfigParser()
conf.read('../config.cfg')

consumer_key = conf.get('twitter_user_timeline', 'consumer_key')
consumer_secret = conf.get('twitter_user_timeline', 'consumer_secret')
access_key = conf.get('twitter_user_timeline', 'access_token_key')  
access_secret = conf.get('twitter_user_timeline', 'access_token_secret') 

def str_to_date_jp(obj_datetime):
    return str(pytz.utc.localize(obj_datetime).astimezone(pytz.timezone('Asia/Tokyo')))

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, str_to_date_jp(tweet.created_at), tweet.text] for tweet in alltweets]

    #write the csv
    with open('tweets_%s.csv' % screen_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("train_yamanote")