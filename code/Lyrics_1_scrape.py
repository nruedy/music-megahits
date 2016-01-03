# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup, Comment
import re
import pandas as pd
import os, os.path
import datetime
import time
import json
import Billboard_3a_clean_track_data_16_01_01b as BBclean



def get_lyrics(start=0, end=None, input_filename='../data/billboard_tracks.pkl'):
    '''
    INPUTS: integer (start), integer (end), string (input_filepath)
    OUTPUTS: None
    DESC: Reads in listing of tracks and writes text files containing track lyrics.
    '''
    df = pd.read_pickle(input_filename)

    artists = df.artist_orig.values
    songs = df.song_orig.values
    filenames = df.filename.values
    tracks = zip(artists, songs, filenames)
    tracks = tracks[ start : end ]

    # set counter to keep track of progress (it adds one right away, so becomes 0 for the first entry)
    count = -1
    tot_num_files = len(tracks)
    Lyrics_path = '../data/lyrics/'
    downloaded = len(os.walk(Lyrics_path).next()[2])
    downloaded_start = downloaded


    for track in tracks:
        artist, song, filename = track
        count += 1
        if count % 20 == 0:
            downloaded_prev = downloaded
            downloaded = len(os.walk(Lyrics_path).next()[2])
            print '{0} / {1}, {2} just added, {3} new so far'.format(count,
                                                         tot_num_files,
                                                         downloaded - downloaded_prev,
                                                         downloaded - downloaded_start)

        # check if lyrics are in folder:
        filepath = '../data/lyrics/{0}.json'.format(filename)
        if os.path.exists(filepath):
            continue

        # generate artist and song strings for searching
        # Find the track, trying various search combinations

        song = BBclean.fix_song_typos(song)

        # create different versions of artist and song for searching

        search_songs = [song]
        search_artists = [artist]

        feat_index = artist.lower().find(' feat')
        if feat_index != -1:
            search_artists.append(artist[:feat_index])

        if clean_strings(artist) not in search_artists:
            search_artists.append(clean_strings(artist))

        if remove_stopwords(artist) not in search_artists:
            search_artists.append(remove_stopwords(artist))

        paren_index = song.find(' (')
        if paren_index != -1:
            search_songs.append(song[:paren_index])

        if clean_strings(song) not in search_songs:
            search_songs.append(clean_strings(song))

        if remove_stopwords(song) not in search_songs:
            search_songs.append(remove_stopwords(song))

        # initialize results as empty dict
        results = dict()

        # Run search with each combination of artist and song, first in songlyrics.com, then lyrics.com

        for search_artist in search_artists:
            for search_song in search_songs:
                if len(results) != 5:
                    results = run_search_songlyrics(search_artist, search_song, count)

        for search_artist in search_artists:
            for search_song in search_songs:
                if len(results) != 5:
                    results = run_search_lyrics(search_artist, search_song, count)

        # Write the file as a .json

        try:
            if len(results) == 5:
                with open(filepath, 'w') as outfile:
                    json.dump(results, outfile)
        except Exception as inst:
            print "Exception: Error writing file", inst, artist, song, str(count)
            # get current time stamp for error log
            tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")
            with open('../data/lyrics_error_logs/songlyrics.csv', 'a') as outfile:
                outfile.write(artist + '`' + song + '`' + 'Exc - Error Writing: ' + str(inst) +
                                '`' + tmstmp + '`' + str(count) + '\n')


def transform_for_url(txt):
    '''
    INPUTS: string
    OUTPUTS: string
    DESC: Transforms artist and song text to replace spaces with dashes, to create urls
    '''
    # replace spaces with dashes
    return re.sub(' ', '-', clean_strings(txt))


def transform_for_search(txt):
    '''
    INPUTS: string
    OUTPUTS: string
    DESC: Transforms artist and song text to replace spaces with plusses, to create urls to run searches
    '''
    # replace spaces with plusses
    return re.sub(' ', '+', clean_strings(txt))


def clean_strings(txt):
    '''
    INPUTS: string
    OUTPUTS: string
    DESC: removes punctuation, makes text lowercase, and removes extra white space
    '''
    # replace & with 'and'
    txt = re.sub('&', 'and', txt)
    # replace ' with ' ' Note: It may be beneficial to run with and without (I already ran without)
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


def run_search_songlyrics(artist, song, count):
    try:
        soup = search_songlyrics_dot_com(artist, song)
        if soup is not None:
            results = extract_lyrics(soup, source='SongLyrics.com')
        else:
            results = dict()
    except Exception as inst:
        results = dict()

        print "Exception: SongLyrics.com error", inst, artist, song, str(count)
        # get current time stamp for error log
        tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")
        with open('../data/lyrics_error_logs/songlyrics.csv', 'a') as outfile:
            outfile.write(artist + '`' + song + '`' + 'Exc - SongLyrics.com: ' + str(inst) +
                            '`' + tmstmp + '`' + str(count) + '\n')
    return results


def run_search_lyrics(artist, song, count):
    try:
        soup = search_lyrics_dot_com(artist, song)
        if soup is not None:
            results = extract_lyrics(soup, source='Lyrics.com')
        else:
            results = dict()
    except Exception as inst:
        print "Exception: Lyrics.com error", inst, artist, song, str(count)
        # get current time stamp for error log
        tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")
        with open('../data/lyrics_error_logs/songlyrics.csv', 'a') as outfile:
            outfile.write(artist + '`' + song + '`' + 'Exc - Lyrics.com: ' + str(inst) +
                            '`' + tmstmp + '`' + str(count) + '\n')
    return results


def search_songlyrics_dot_com(artist, song):
    '''
    INPUTS: two strings (artist name, song name)
    OUTPUTS: lyrics as a string, or None if unsuccessful
    DESC: try constructing the url for lyrics.com, and if that doesn't work, run a search on the site
    '''
    url = 'http://www.songlyrics.com/{0}/{1}-lyrics/'.format(transform_for_url(artist), transform_for_url(song))
    html_string = requests.get(url).content
    soup = BeautifulSoup(html_string, 'html.parser')
    # uncomment the lines below to enable search
    # right now, search is commented out because the site's search is very flexible, and it will almost
    # always return a result. I need to run an additional check to make sure the result is the correct one.
    '''
    # need to check what conditional statement below would work. unlike lyrics.com, I don't think it returns ''.
    if html_string == '':
        # make search request on songlyrics.com
        keyword_for_search = '{0}+{1}'.format(transform_for_search(artist), transform_for_search(song))
        url = 'http://www.songlyrics.com/index.php?section=search&searchW={0}&submit=Search'.format(keyword_for_search)
        search_results = requests.get(url, allow_redirects=False)

        #check if search_results are empty:
        if search_results == '':
            return None

        soup_search_results = BeautifulSoup(search_results.content, 'html.parser')

        # take first entry
        search_results_link = soup_search_results.find('div',{'class': 'serpresult'}).find_all('a')[0].get('href')
        url = search_results_link
        html_string = requests.get(url).content
        soup = BeautifulSoup(html_string, 'html.parser')
    '''
    if soup.find('p',{'id': 'songLyricsDiv'}).text[:18] == 'Sorry, we have no ':
        return None

    # if it found the website, but there are no lyrics
    if soup.find('p',{'id': 'songLyricsDiv'}) is None:
        return None

    return soup.find('p',{'id': 'songLyricsDiv'}).text


def search_lyrics_dot_com(artist, song):
    '''
    INPUTS: two strings (artist name, song name)
    OUTPUTS: lyrics as a string, or None if unsuccessful
    DESC: try constructing the url for lyrics.com, and if that doesn't work, run a search on the site
    '''
    url = 'http://www.lyrics.com/{0}-lyrics-{1}.html'.format(transform_for_url(song), transform_for_url(artist))
    html_string = requests.get(url, allow_redirects=False).content
    # commenting out search, because it may not be reliable
    '''
    if html_string == '':
        # make search request on lyrics.com
        keyword_for_search = '{0}+{1}'.format(transform_for_search(song), transform_for_search(artist))
        url = 'http://www.lyrics.com/search.php?keyword={0}&what=all'.format(keyword_for_search)
        search_results = requests.get(url, allow_redirects=False)

        #check if search_results are empty:
        if search_results == '':
            return None

        soup_search_results = BeautifulSoup(search_results.content, 'html.parser')

        # take first entry
        search_results_link = soup_search_results.find('div',{'id': 'rightcontent'}).find_all('a')[0].get('href')
        url = 'http://www.lyrics.com' + search_results_link
        html_string = requests.get(url).content
    '''
    # if it found the website through constructing the url, but there are no lyrics
    soup = BeautifulSoup(html_string, 'html.parser')
    if soup.find('div',{'id': 'lyrics'}) is None:
        return None

    return soup.find('div',{'id': 'lyrics'}).text


def extract_lyrics(lyrics, source):
    '''
    INPUTS: soup object, bool
    OUTPUTS: dictionary
    DESC: clean lyrics and count stanzas / lines, return as dictionary
    '''
    results = dict()
    null_result = dict()
    results['source'] = source
    lyrics = lyrics.replace('\r','')
    results['stanzas'] = lyrics.count('\n\n') + 1
    lyrics = lyrics.replace('\n\n','\n')
    results['lines'] = lyrics.count('\n') + 1
    lyrics = lyrics.replace('\n',' ')
    # check that lyrics exist
    if (len(lyrics) < 100) & (lyrics.lower().find('do not have the lyrics') != -1):
        return null_result
    if (len(lyrics) < 100) & (lyrics.lower().find('sorry, we have no') != -1):
        return null_result
    if (len(lyrics) < 30) & (lyrics.lower().find('instrumental') != -1):
        results['instrumental'] = True
    else:
        results['instrumental'] = False
    # remove contributor information
    if source == 'Lyrics.com':
        index_contrib = lyrics.rfind('---')
        if index_contrib == -1:
            index_contrib = None
        lyrics = lyrics[:index_contrib]
    results['lyrics'] = lyrics

    return results





if __name__ == '__main__':
    get_lyrics()




