from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

from musicXmatch import musicXmatch
import re
import time
import sys

status_codes = {200	: 'OK: Success!',
                304	: 'Not Modified: There was no new data to return.',
                400	: 'Bad Request: The request was invalid or cannot be otherwise served. An accompanying error message will explain further. In API v1.1, requests without authentication are considered invalid and will yield this response.',
                401	: 'Unauthorized: Authentication credentials were missing or incorrect. Also returned in other circumstances, for example all calls to API v1 endpoints now return 401 (use API v1.1 instead).',
                403	: 'Forbidden: The request is understood, but it has been refused or access is not allowed. An accompanying error message will explain why. This code is used when requests are being denied due to update limits. Other reasons for this status being returned are listed alongside the response codes in the table below.',
                404	: 'Not Found: The URI requested is invalid or the resource requested, such as a user, does not exists. Also returned when the requested format is not supported by the requested method.',
                406	: 'Not Acceptable: Returned by the Search API when an invalid format is specified in the request.',
                410	: 'Gone: This resource is gone. Used to indicate that an API endpoint has been turned off. For example: “The Twitter REST API v1 will soon stop functioning. Please migrate to API v1.1.”',
                420	: 'Enhance Your Calm: Returned by the version 1 Search and Trends APIs when you are being rate limited.',
                422	: 'Unprocessable Entity: Returned when an image uploaded to POST account / update_profile_banner is unable to be processed.',
                429	: 'Too Many Request: Returned in API v1.1 when a request cannot be served due to the application’s rate limit having been exhausted for the resource. See Rate Limiting in API v1.1.',
                500	: 'Internal Server Error: Something is broken. Please post to the developer forums so the Twitter team can investigate.',
                502	: 'Bad Gateway: Twitter is down or being upgraded.',
                503	: 'Service Unavailable: The Twitter servers are up, but overloaded with requests. Try again later.',
                504	: 'Gateway timeout: The Twitter servers are up, but the request couldn’t be serviced due to some failure within our stack. Try again later.'}

errors = { 32 : 'Could not authenticate you: Your call could not be completed as dialed.',
           34 : 'Sorry, that page does not exist: Corresponds with an HTTP 404 - the specified resource was not found.',
           64 : 'Your account is suspended and is not permitted to access this feature: Corresponds with an HTTP 403 — the access token being used belongs to a suspended user and they can’t complete the action you’re trying to take',
           68 : 'The Twitter REST API v1 is no longer active. Please migrate to API v1.1. https://dev.twitter.com/rest/public: Corresponds to a HTTP request to a retired v1-era URL.',
           88 : 'Rate limit exceeded: The request limit for this resource has been reached for the current rate limit window.',
           89 : 'Invalid or expired token: The access token used in the request is incorrect or has expired. Used in API v1.1',
           92 : 'SSL is required: Only SSL connections are allowed in the API, you should update your request to a secure connection. See how to connect using SSL',
          130 : 'Over capacity: Corresponds with an HTTP 503 - Twitter is temporarily over capacity.',
          131 : 'Internal error: Corresponds with an HTTP 500 - An unknown internal error occurred.',
          135 : 'Could not authenticate you: Corresponds with a HTTP 401 - it means that your oauth_timestamp is either ahead or behind our acceptable range',
          161 : 'You are unable to follow more people at this time: Corresponds with HTTP 403 — thrown when a user cannot follow another user due to some kind of limit',
          179 : 'Sorry, you are not authorized to see this status: Corresponds with HTTP 403 — thrown when a Tweet cannot be viewed by the authenticating user, usually due to the tweet’s author having protected their tweets.',
          185 : 'User is over daily status update limit: Corresponds with HTTP 403 — thrown when a tweet cannot be posted due to the user having no allowance remaining to post. Despite the text in the error message indicating that this error is only thrown when a daily limit is reached, this error will be thrown whenever a posting limitation has been reached. Posting allowances have roaming windows of time of unspecified duration.',
          187 : 'Status is a duplicate: The status text has been Tweeted already by the authenticated account.',
          215 : 'Bad authentication data: Typically sent with 1.1 responses with HTTP code 400. The method requires authentication but it was not presented or was wholly invalid.',
          226 : 'This request looks like it might be automated. To protect our users from spam and other malicious activity, we can’t complete this action right now: We constantly monitor and adjust our filters to block spam and malicious activity on the Twitter platform. These systems are tuned in real-time. If you get this response our systems have flagged the Tweet or DM as possibly fitting this profile. If you feel that the Tweet or DM you attempted to create was flagged in error, please report the details around that to us by filing a ticket at https://support.twitter.com/forms/platform.',
          231 : 'User must verify login: Returned as a challenge in xAuth when the user has login verification enabled on their account and needs to be directed to twitter.com to generate a temporary password.',
          251 : 'This endpoint has been retired and should not be used: Corresponds to a HTTP request to a retired URL.',
          261 : 'Application cannot perform write actions: Corresponds with HTTP 403 — thrown when the application is restricted from POST, PUT, or DELETE actions. See How to appeal application suspension and other disciplinary actions.',
          271 : 'You can’t mute yourself: Corresponds with HTTP 403. The authenticated user account cannot mute itself.',
          272 : 'You are not muting the specified user: Corresponds with HTTP 403. The authenticated user account is not muting the account a call is attempting to unmute.',
          354 : 'The text of your direct message is over the max character limit: Corresponds with HTTP 403. The message size exceeds the number of characters permitted in a direct message.'}


def remove_emoji(data):
    try:
    # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
    # UCS-2
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)

target = {}
bot = {}
mm = []
api = []

class StreamListener(tweepy.StreamListener):

    def on_status(self,status):

        if target['tag'] in status.text.lower():

            lyrics = status.text
            lyrics = remove_emoji(lyrics)
            lyrics = lyrics.replace(target['tag'],'')

            if bot['name'] is 'sirius':
                song_list = mm.get_song_list_by_lyrics(lyrics)

                print('Select one of the following options: ')

                for i in range(len(song_list)):
                    print('[{:>2}'.format(i) + '] : ' + song_list[i][1] + ' by ' + song_list[i][0])

                option = ''

                while option is '' :
                    inp = input('\n>> ')
                    if inp:
                        option = int(inp)
                        if option >= len(song_list):
                            option = ''

                    if option is '':
                        print("Please select a valid option")

                song = song_list[option]

            elif bot['name'] is 'bender':
                song = mm.get_song_by_lyrics(lyrics)
                time.sleep(0.5)

            if song is not 'error':

                tweet = '@' + target['username'] + ' ' + song[0] + ' - ' + song[1] + ' ' + target['tag']
                api.update_status(tweet, in_reply_to_status_id = status.id)
                print('Posted the following tweet: ')
                print(tweet)
                sys.exit(0)

            else:
                print('Error')

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        time.sleep(3000)
        return False

    def on_timeout(self):
        print('Timeout...')
        time.sleep(3000)
        return False


class twitterBot:

    def __init__(self, botData, targetData):

        global bot
        bot = botData

        global target
        target = targetData

        global mm
        mm = musicXmatch()

        self.bot = botData['name']
        auth = tweepy.OAuthHandler(botData['consumer_key'], botData['consumer_secret'])
        auth.secure = True
        auth.set_access_token(botData['access_token'], botData['access_token_secret'])

        global api
        api = tweepy.API(auth)

        self.target = targetData

    def track(self):

        self.mylistener = StreamListener()
        mystream = tweepy.Stream(auth = api.auth, listener = self.mylistener)
        mystream.filter(follow = [self.target['userid']])
