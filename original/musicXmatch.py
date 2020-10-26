#!/usr/bin/python3

import json
from urllib.request import urlopen

class musicXmatch:

    def __init__(self):

        self.musixmatchAPI     = "http://api.musixmatch.com/ws/1.1/"
        self.musixmatchAPI_KEY = ""

        self.codes = {200 : "The request was successful.", \
                      400 : "The request had bad syntax or was inherently impossible to be satisfied.", \
                      401 : "Authentication failed, probably because of invalid/missing API key.", \
                      402 : "The usage limit has been reached, either you exceeded per day requests limits or your balance is insufficient.", \
                      403 : "You are not authorized to perform this operation.", \
                      404 : "The requested resource was not found.", \
                      405 : "The requested method was not found.", \
                      500 : "Ops. Something were wrong.", \
                      503 : "Our system is a bit busy at the moment and your request can’t be satisfied.]"}


    def query(self, queryString):

        try:
            htmlResponse = urlopen(queryString).read()
            response = json.loads(htmlResponse.decode(encoding='UTF-8'))

            code = response['message']['header']['status_code']

            if code == 200:
                return response['message']['body']
            else:
                print(self.codes[code])
                print('Query: ' + queryString)
                return 'error'
        except:
            return 'error'

    def get_song_by_id(self, id):

        queryString = self.musixmatchAPI + "track.get?apikey=" + self.musixmatchAPI_KEY + "&track_id=" + str(id)

        response = self.query(queryString)

        if response == 'error':
            return response
        else:
            song = (response['track']['track_name'], response['track']['artist_name'])
            return song

    def get_lyrics_by_id(self, id):

        queryString = self.musixmatchAPI + "track.lyrics.get?apikey=" + self.musixmatchAPI_KEY + "&track_id=" + str(id)

        response = self.query(queryString)

        if response == 'error':
            return response
        else:
            return response['lyrics']['lyrics_body']



    def get_lyrics_by_artist_and_title(self, artist, title):

        queryString = self.musixmatchAPI + "matcher.lyrics.get?apikey=" + self.musixmatchAPI_KEY + "&q_track=" + title.replace(" ","%20") + "&q_artist=" + artist
        response = self.query(queryString)

        if response == 'error':
            return response
        else:
            lyrics = response['lyrics']['lyrics_body']
            return lyrics[:lyrics.rfind("...")]


    def get_artist_by_title(self, title):

        queryString = self.musixmatchAPI + "track.search?apikey=" + self.musixmatchAPI_KEY + "&q_track=" + title.replace(" ","%20") + "&format=json&f_has_lyrics=1&s_track_rating=desc"
        response = self.query(queryString)

        if response == 'error':
            return response
        else:
            artist_list = []
            for artist in response['track_list']:
                artist_list.append(artist['track']['artist_name'])
            return artist_list


    def get_song_list_by_lyrics(self, lyrics):

        queryString = self.musixmatchAPI + "track.search?apikey=" + self.musixmatchAPI_KEY + "&q_lyrics=" + lyrics.replace(" ","%20") + "&format=json&f_has_lyrics=1&s_track_rating=desc&page_size=15"
        response = self.query(queryString)

        if response == 'error':
            return []
        else:
            song_list = []
            for track in response['track_list']:
                title = track['track']['track_name']

                s = title.find('(')
                if s > 0:
                    title = title[:s]

                s = title.find('[')
                if s > 0:
                    title = title[:s]

                song_list.append((track['track']['artist_name'], title.strip(), track['track']['track_id']))
            return song_list

    def get_song_id_list_by_lyrics(self, lyrics):

        queryString = self.musixmatchAPI + "track.search?apikey=" + self.musixmatchAPI_KEY + "&q_lyrics=" + lyrics.replace(" ","%20") + "&format=json&f_has_lyrics=1&s_track_rating=desc&page_size=15"
        response = self.query(queryString)

        if response == 'error':
            return []
        else:
            song_id_list = []
            for track in response['track_list']:
                id = track['track']['track_id']
                song_id_list.append(id)
            return song_id_list

    def get_song_by_lyrics(self, lyrics):

        lyrics = lyrics.replace('\n',' ').replace(',','').replace('.','').lower()
        song_list = self.get_song_list_by_lyrics(lyrics)

        if len(song_list) == 0:
            return 'error'
        else:
            return song_list[0]

    def get_song_by_lyrics_check(self, lyrics):

        lyrics = lyrics.replace('\n',' ').replace(',','').replace('.','').lower()
        song_list = self.get_song_list_by_lyrics(lyrics)

        if len(song_list) == 0:
            return 'error'
        else:
            for song in song_list:
                lyrics_guess = self.get_lyrics_by_id(song[2])

                if lyrics_guess != 'error':
                    lyrics_guess = lyrics_guess.replace('\n',' ').replace(',','').replace('.','').lower()

                    if lyrics_guess.find(lyrics) != -1:
                        return song
            return song_list[0]
