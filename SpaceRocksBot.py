import json
from urllib.request import urlopen
import tweepy
import re
import time

# DATA ---------------------------------------------------------------------------------------------------------------

# Musix Match API data
musixmatchAPI_KEY = ""

# Twitter account API data
twitterConsumerKey = ""
twitterConsumerSecret = ""
twitterAccessTokenKey = ""
twitterAccessTokenSecret = ""
twitterAPI = None

# Target
target = {"userID"   : "", # Something like 4852873365
          "userName" : "", # Something like do_the_bender
          "tag"      : ""} # Something like #spacerocks.12

# PROGRAM ------------------------------------------------------------------------------------------------------------

# Gets a song list given its lyrics. Uses Musix Match API
def getSongListByLyrics(lyrics):
    queryString = f"http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmatchAPI_KEY}&q_lyrics={lyrics.replace(' ','%20')}&format=json&f_has_lyrics=1&s_track_rating=desc&page_size=15"
    response = json.loads(urlopen(queryString).read().decode(encoding='UTF-8'))

    try:
        if response['message']['header']['status_code'] == 200:
            return response['message']['body']['track_list']
        else:
            return []
    except KeyError:
        return []


# Removes everything that comes after a (, [ or - from a string
def removeExtras(string):
    return string.split('(')[0].split('[')[0].split('-')[0].strip()


# Removes emojis from a string
def removeEmoji(string):
    try:
        emojiPattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])') # UCS-4
    except re.error:
        emojiPattern = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])') # UCS-2
    return emojiPattern.sub('', string)


# Twitter stream listener
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(f"Got new status {status}")
        if target['tag'] in status.text.lower():
            lyrics = removeEmoji(status.text).replace(target['tag'], '')
            songList = getSongListByLyrics(lyrics)

            if songList:
                artistName = removeExtras(songList[0]['track']['artist_name'])
                trackName = removeExtras(songList[0]['track']['track_name'])
                tweet = '@' + target['userName'] + ' ' + artistName + ' - ' + trackName + ' ' + target['tag']
                time.sleep(0.5)
                twitterAPI.update_status(tweet, in_reply_to_status_id = status.id)
                print("Posted the following tweet:\n" + tweet)
            else:
                print("Didn't find any matching songs!")

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        time.sleep(3000)
        return False

    def on_timeout(self):
        print('Timeout...')
        time.sleep(3000)
        return False


# Main program
if __name__ == "__main__":
    auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
    auth.secure = True
    auth.set_access_token(twitterAccessTokenKey, twitterAccessTokenSecret)
    twitterAPI = tweepy.API(auth)
    listener = StreamListener()
    print(f"Started tracking @{target['userName']}...")
    stream = tweepy.Stream(auth = twitterAPI.auth, listener = listener)
    stream.filter(follow = [target['userID']])
