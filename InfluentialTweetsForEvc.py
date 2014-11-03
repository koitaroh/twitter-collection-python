# InfluentialTweetsForEvc.py
# Last Update: 10/23/2014
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Extracts influential tweets
# Parameters: 
# Require: tweepy
# 

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey = 'JlGcmVwZA8AuqnMThGSaSEMGp'
csecret = 'AIK2HozQ15H0O1z5k0XQhe1CH3fRH9pAtAXfVYFJCSS6oNRIKm'
atoken = '11753002-0mQ52rQnLHOsmj0gheIavMhYqEOSAF8PKf0VPwkE8'
asecret = 'vqNBCXcHCJ3r29ONH4snDT1pVdm30Et30vIReY0AyfDtQ'

class listener(StreamListener):

	def on_data(self, data):
		try:
			# print data

			tweet = data.split(',"text":"')[1].split('","source')[0]
			print tweet

			saveThis = str(time.time())+'::'+tweet

			saveFile = open('twitDB2.csv', 'a')
			saveFile.write(saveThis)
			saveFile.write('\n')
			saveFile.close()
			return True
		except BaseException, e:
			print 'failed ondata,',str(e)
			time.sleep(5)

	def on_error(self, status):
		print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])