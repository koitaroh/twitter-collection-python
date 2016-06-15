# Last Update: 2015-10-15
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Objective: Collect tweet and store into database

from tweepy import Stream

import time, datetime, json, sys, calendar, configparser, traceback, pymysql, importlib, tweepy

# Constants                                                                                                                                                     
MECAB_MODE = 'mecabrc'
PARSE_TEXT_ENCODING = 'utf-8'

# Reload sys module in order to set default encoding as utf-8.

d = datetime.datetime.today()
conf = configparser.ConfigParser()
conf.read('../config.cfg')
print("initiated at:" + d.strftime("%Y-%m-%d %H:%M:%S"))
i = 0


table_name = "tweet_table_ec2_1_" + d.strftime("%Y%m%d%H%M%S")

consumer_key = conf.get('twitter_1', 'consumer_key')
consumer_secret = conf.get('twitter_1', 'consumer_secret')
access_token_key = conf.get('twitter_1', 'access_token_key')
access_token_secret = conf.get('twitter_1', 'access_token_secret')

local_db = {
            "host": conf.get('ec2_1', 'host'),
            "user": conf.get('ec2_1', 'user'),
            "passwd": conf.get('ec2_1', 'passwd'),
            "db_name": conf.get('ec2_1', 'db_name'),
            }   


# Function to convert "created at" in GMT to JST
def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time_local))

class listener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        global i
        try:
            tweet = json.loads(data + "\n","utf-8")
            if tweet['geo']:
                raw_tweet = tweet['text'] # convert from Unicode

                if "I'm at" not in raw_tweet and "きつねかわいい" not in raw_tweet:
                    datetimeJST = YmdHMS(tweet['created_at']) # convert datetime to local datetime.
                    raw_tweet = filter(raw_tweet)
                    # print("%d" % i +' ' + datetimeJST +': '+ raw_tweet + '\r')
                    i = i + 1

                    row = [

                        tweet['id'],
                        datetimeJST,
                        tweet['user']['screen_name'],
                        tweet['user']['id_str'],
                        tweet['geo']['coordinates'][1],
                        tweet['geo']['coordinates'][0],
                        raw_tweet,
                        tweet['lang']

                        ]
                    tweet_table_dict = {
                        "tweet_id": tweet['id'],
                        "tweeted_at": datetimeJST,
                        "user_name": tweet['user']['screen_name'],
                        "user_id": tweet['user']['id_str'],
                        "x": tweet['geo']['coordinates'][1],
                        "y": tweet['geo']['coordinates'][0],
                        "text": raw_tweet,
                        "lang": tweet['lang']
                        }

                    insert_into_tweet_table(local_db, tweet_table_dict)
                    
                # writer.writerow(row)
        # ignore type error
        except ValueError:
            pass
        except BaseException as e:
            print('failed ondata,',str(e))
            # time.sleep(5)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        else:
            print('Got an error with status code: ' + str(status_code))
            return True # To continue listening

 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

def filter(text):
    # "RT @user:"を削除
    if "RT " in text:
        text = text.split(":", 1)[1]
    # "@user"を削除
    # if "@" in text and " " in text:
    if text[0] == "@":
        text = text.split(" ", text.count("@"))[-1]
    # "#tag"を削除
    if "#" in text:
        text = text.split("#", 1)[0]
    # "URL"を削除
    if "http" in text:
        text = text.split("http", 1)[0]
    text = text.replace('\n','')
    text = text.replace('\r','')
    text = text.replace("\'",' ')
    text = text.replace("\"",' ') 
    text = text.replace("\\",' ') 
    text = text.rstrip()
    return text

def create_db(db_info): 
    connector = pymysql.connect(
        host = db_info["host"],
        user = db_info["user"],
        passwd = db_info["passwd"],
        charset = "utf8mb4"
        )
    cursor = connector.cursor()
    sql = """
    CREATE DATABASE IF NOT EXISTS
        %s
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    ;
    """ %(db_info["db_name"])
    cursor.execute(sql)
    connector.commit()
    cursor.close()
    connector.close()
    return True

def execute_sql(sql, db_info, is_commit = False):
    connection = pymysql.connect(host = db_info["host"],
                                 user = db_info["user"],
                                 passwd = db_info["passwd"],
                                 db = db_info["db_name"],
                                 charset = "utf8mb4",
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        if is_commit:
            connection.commit()
        cursor.close()
    finally:
        connection.close()

def create_tweet_table(db_info):
    sql = """
    CREATE TABLE IF NOT EXISTS
        %s(
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            tweet_id BIGINT,
            tweeted_at DATETIME,
            user_name VARCHAR(50),
            user_id BIGINT,
            x DECIMAL(12,8),
            y DECIMAL(12,8),
            text VARCHAR(255),
            lang VARCHAR(4),
            words VARCHAR(255)
        )
        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    ;
    """ %table_name
    execute_sql(sql, db_info, is_commit = True)
    return True

def insert_into_tweet_table(db_info, tweet_table_dict):
    sql = """                                                                                                                                                     
    INSERT INTO                                                                                                                                                   
        %s                                                                                                                                         
    VALUES(                                                                                                                                                       
        NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NULL
        )                                                                                                                                                         
    ;                                                                                                                         
    """ %(
        table_name,
        tweet_table_dict["tweet_id"],
        tweet_table_dict["tweeted_at"],
        tweet_table_dict["user_name"],
        tweet_table_dict["user_id"],
        tweet_table_dict["x"],
        tweet_table_dict["y"],
        tweet_table_dict["text"],
        tweet_table_dict["lang"]
        )
    execute_sql(sql, db_info, is_commit = True)
    return True

def main():
    while True: 
        try:
            # From mysql_tools.py
            create_db(local_db)
            create_tweet_table(local_db)

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token_key, access_token_secret)

            twitterStream = tweepy.Stream(auth, listener())
            twitterStream.filter(locations=[122.933198,24.045416,153.986939,45.522785])

                                                                                                                                                     
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            # Try reconnection
            time.sleep(60)
            twitterStream = Stream(auth, listener())

if __name__ == '__main__':
    main()