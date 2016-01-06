# -*- coding: utf-8 -*-
import json
import pandas as pd
import datetime
import time
import os, os.path
import requests
from pyechonest import config
from pyechonest import song
import Billboard_3a_clean_track_data_16_01_01b as BBclean
import re



timeout_sec = 20  # set timeout parameter for echonest song.search() and requests.get()
config.CALL_TIMEOUT = timeout_sec

class EchonestGetter(object):
    '''
    INPUTS: artist and song search terms
    OUTPUTS: None
    DESC: writes a json file with track information
    '''
    def __init__(self, artist, song, filename, tmstmp, track_num):
        self._artist = artist
        self._song = song
        self._filename = filename
        self._tmstmp = tmstmp
        self._track_num = track_num

    def run_search(self, search_artist, search_song):
        try:
            search_results = song.search(artist=search_artist, title=search_song, buckets=['song_hotttnesss'])
        except Exception as inst:
            search_results = []

            print "Exception (basic search):", inst, "ID#:", self._track_num
            with open('../data/echonest_error_logs/echonest_errors.csv', 'a') as outfile:
                outfile.write(self._artist + '`' + self._song + '`' + 'Exc 1: ' + str(inst) +
                                '`' + self._tmstmp + '\n')
            time.sleep(1.0/3.0)

        return search_results

    def getdata(self):
        filepath = '../data/echonest/{0}.json'.format(self._filename)
        null_filepath = '../data/echonest_null/{0}.json'.format(self._filename)
        error_filepath = '../data/echonest_null_results/{0}.csv'.format(self._tmstmp)

        # Skip files retreived from a previous run
        if os.path.exists(filepath):
            return

        # Skip files which could not be found on a previous run
        if os.path.exists(null_filepath):
            return

        # Find the track, trying various search combinations

        self._song = BBclean.fix_song_typos(self._song)

        # create different versions of artist and song for searching

        search_songs = [self._song]
        search_artists = [self._artist]

        feat_index = self._artist.lower().find(' feat')
        if feat_index != -1:
            search_artists.append(self._artist[:feat_index])

        if clean_strings(self._artist) not in search_artists:
            search_artists.append(clean_strings(self._artist))

        if remove_stopwords(self._artist) not in search_artists:
            search_artists.append(remove_stopwords(self._artist))

        paren_index = self._song.find(' (')
        if paren_index != -1:
            search_songs.append(self._song[:paren_index])

        if clean_strings(self._song) not in search_songs:
            search_songs.append(clean_strings(self._song))

        if remove_stopwords(self._song) not in search_songs:
            search_songs.append(remove_stopwords(self._song))

        # Run search with each combination of artist and song
        search_results = []
        for search_artist in search_artists:
            for search_song in search_songs:
                if search_results == []:
                    search_results = self.run_search(search_artist, search_song)


        # Write missing track data
        if search_results == []:
            with open(error_filepath, 'a') as outfile:
                outfile.write(self._artist + '|' + self._song + '|' + str(self._track_num) + '\n')
            with open(null_filepath, 'w') as outfile:
                json.dump(search_results, outfile)
            time.sleep(1.0/3.0)
            return

        try:
            # get all the song objects that share the title with the most relevant song object
            top_results = [track for track in search_results if track.title == search_results[0].title]
            # of the songs with the same title, take the one with greatest "hotttnesss"
            top_result = sorted(top_results, key=lambda x: x.song_hotttnesss)[-1]
            results = dict()
            results['id'] = top_result.id
            results['title'] = top_result.title
            results['artist_id'] = top_result.artist_id
            results['artist_name'] = top_result.artist_name
            results['audio_summary'] = top_result.audio_summary
            results['song_type'] = top_result.song_type
            results['artist_familiarity'] = top_result.artist_familiarity
            results['artist_hotttnesss'] = top_result.artist_hotttnesss
            results['artist_location'] = top_result.artist_location
            results['song_currency'] = top_result.song_currency
            results['song_discovery'] = top_result.song_discovery
            results['song_hotttnesss'] = top_result.song_hotttnesss

            #get detailed data
            url = results['audio_summary']['analysis_url']
            data = requests.get(url, timeout=timeout_sec).content
            results['analysis'] = json.loads(data)

            with open(filepath, 'w') as outfile:
                json.dump(results, outfile)

        except Exception as inst:
            print "Exception (write): ", inst, "ID#:", self._track_num
            with open('../data/echonest_error_logs/echonest_errors.csv', 'a') as outfile:
                outfile.write(self._artist + '`' + self._song + '`' + 'Exc 2: ' + str(inst) +
                                '`' + self._tmstmp + '\n')
            time.sleep(1.0/3.0)
            return


def clean_strings(txt):
    # replace & with 'and'
    txt = re.sub('&', 'and', txt)
    # replace ' with ' '
    txt = re.sub("'", ' ', txt)
    # remove punctuation
    invalid_punc = '[!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~§]'
    txt = re.sub(invalid_punc, '', txt)
    # remove extra white space and make lowercase
    return ' '.join(txt.lower().split())

def remove_stopwords(txt):    # remove 'a', 'the', and extraneous white space
    # check first if txt has more than one word, because there is an artist called "A"
    if len(txt.split()) == 1:
        return ' '.join(txt.split())
    else:
        return ' '.join([word for word in txt.split() if word.lower() not in ['the', 'a']])


def get_API_data(start=0, end=None, input_filename='../data/billboard_tracks.pkl'):
    '''
    INPUT: path to billboard data
    OUTPUT: None
    DESC: Calls EchoNest API to get track data
    '''
    df = pd.read_pickle(input_filename)

    track_info = zip(df.artist_orig.values, df.song_orig.values, df.filename.values)
    # get subset of data for searches
    track_info = track_info[ start : end ]

    # get current time stamp for error log
    tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")

    count = 0
    tot_num_files = len(track_info)
    EN_path = '../data/echonest/'
    downloaded = len(os.walk(EN_path).next()[2])
    downloaded_start = downloaded

    for track_tuple in track_info:
        echonest_getter = EchonestGetter(track_tuple[0], track_tuple[1], track_tuple[2], tmstmp, count)
        echonest_getter.getdata()

        if count % 20 == 0:
            downloaded_prev = downloaded
            downloaded = len(os.walk(EN_path).next()[2])
            print '{0} / {1}, {2} just added, {3} new so far'.format(count,
                                                                     tot_num_files,
                                                                     downloaded - downloaded_prev,
                                                                     downloaded - downloaded_start)
        count += 1




if __name__ == '__main__':
    get_API_data()
