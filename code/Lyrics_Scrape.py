import requests
from bs4 import BeautifulSoup, Comment
import re
import pandas as pd
import os.path
import datetime
import time
import json



def get_lyrics(start=0, end=None, input_filename='../data/billboard_tracks.pkl'):
    '''
    INPUTS: integer (start), integer (end), string (input_filepath)
    OUTPUTS: None
    DESC: Reads in listing of tracks and writes text files containing track lyrics.
    '''
    df = pd.read_pickle(input_filename)

    #extract these as lists?
    artists = df.artist_clean.values
    songs = df.song_clean.values
    filenames = ['{0}___{1}'.format(artist, song) for artist, song in zip(artists, songs)]
    tracks = zip(artists, songs, filenames)
    tracks = tracks[ start : end ]

   # set counter to keep track of progress (it adds one right away, so becomes 0 for the first entry)
    count = -1


    for track in tracks:
        artist, song, filename = track
        count += 1
        if count % 20 == 0:
            print count, 'records processed'

        # check if lyrics are in folder:
        filepath = '../data/lyrics/{0}.json'.format(filename)
        if os.path.exists(filepath):
            continue

        # check if lyrics are in null folder:
        null_filepath = '../data/lyrics_null/{0}.json'.format(filename)
        if os.path.exists(null_filepath):
            continue

        # initialize results now, so that I can check length after searching lyrics.com
        results = dict()

        # I commented out the lines below because I've already searched lyrics.com, so skipping to save time
        '''
        try:
            soup = search_lyrics_dot_com(artist, song)
            if soup != None:
                results = extract_lyrics(soup, author_info=True)
        except Exception as inst:
            # print "Exception: Lyrics.com error", inst, artist, song, str(count)
            pass
        '''
        if len(results) != 3:
            try:
                soup = search_songlyrics_dot_com(artist, song)
                if soup != None:
                    results = extract_lyrics(soup, author_info=False)
                else:
                    continue
            except Exception as inst:
                print "Exception: SongLyrics.com error", inst, artist, song, str(count)
                # get current time stamp for error log
                tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")
                with open('../data/lyrics_error_logs/songlyrics.csv', 'a') as outfile:
                    outfile.write(artist + '`' + song + '`' + 'Exc 1: ' + str(inst) +
                                    '`' + tmstmp + '`' + str(count) + '\n')


        try:
            if len(results) == 3:
                with open(filepath, 'w') as outfile:
                    json.dump(results, outfile)
        except Exception as inst:
            print "Exception: Error writing file", inst, artist, song, str(count)
            # get current time stamp for error log
            tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")
            with open('../data/lyrics_error_logs/songlyrics.csv', 'a') as outfile:
                outfile.write(artist + '`' + song + '`' + 'Exc 2: ' + str(inst) +
                                '`' + tmstmp + '`' + str(count) + '\n')


def transform_for_url(txt):
    '''
    INPUTS: string
    OUTPUTS: string
    DESC: Transforms artist and song text to replace spaces with dashes, to create urls
    '''
    # remove extra white space and make lowercase
    txt = ' '.join(txt.lower().split())

    # replace spaces with dashes
    return re.sub(' ', '-', txt)


def transform_for_search(txt):
    '''
    INPUTS: string
    OUTPUTS: string
    DESC: Transforms artist and song text to replace spaces with plusses, to create urls to run searches
    '''
    # remove extra white space and make lowercase
    txt = ' '.join(txt.lower().split())

    # replace spaces with plusses
    return re.sub(' ', '+', txt)


def search_lyrics_dot_com(artist, song):
    '''
    INPUTS: two strings (artist name, song name)
    OUTPUTS: lyrics as a string, or None if unsuccessful
    DESC: try constructing the url for lyrics.com, and if that doesn't work, run a search on the site
    '''
    url = 'http://www.lyrics.com/{0}-lyrics-{1}.html'.format(transform_for_url(song), transform_for_url(artist))
    html_string = requests.get(url, allow_redirects=False).content
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

    # if it found the website through constructing the url, but there are no lyrics
    soup = BeautifulSoup(html_string, 'html.parser')
    if soup.find('div',{'id': 'lyrics'}) == None:
        with open(null_filepath, 'w') as outfile:
            json.dump('', outfile)
        return None

    return soup.find('div',{'id': 'lyrics'}).text


def search_songlyrics_dot_com(artist, song):
    '''
    INPUTS: two strings (artist name, song name)
    OUTPUTS: lyrics as a string, or None if unsuccessful
    DESC: try constructing the url for lyrics.com, and if that doesn't work, run a search on the site
    '''
    url = 'http://www.songlyrics.com/{0}/{1}-lyrics/'.format(transform_for_url(artist), transform_for_url(song))
    html_string = requests.get(url, allow_redirects=False).content
    soup = BeautifulSoup(html_string, 'html.parser')
    if soup.find('p',{'id': 'songLyricsDiv'}).text[:18] == 'Sorry, we have no ':
        return None
        # remove the return None, and uncomment the lines below to enable search
        # right now, search is commented out because the site's search is very flexible, and it will almost
        # always return a result. I need to run an additional check to make sure the result is the correct one.
        '''
        # make search request on lyrics.com
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

    # if it found the website, but there are no lyrics
    if soup.find('p',{'id': 'songLyricsDiv'}) == None:
        with open(null_filepath, 'w') as outfile:
            json.dump('', outfile)
        return None

    return soup.find('p',{'id': 'songLyricsDiv'}).text


def extract_lyrics(lyrics, author_info=False):
    '''
    INPUTS: soup object, bool
    OUTPUTS: dictionary
    DESC: clean lyrics and count stanzas / lines, return as dictionary
        author_info bool controls whether the code for removing author info runs
        (The code is needed for lyrics.com, but not songlyrics.com.)
    '''
    #TODO: [Chorus] [intro] [outro] [4x]
    #TODO: \u2019 \u201c \u201d
    results = dict()
    lyrics = lyrics.replace('\r','')
    results['stanzas'] = lyrics.count('\n\n') + 1
    lyrics = lyrics.replace('\n\n','\n')
    results['lines'] = lyrics.count('\n') + 1
    lyrics = lyrics.replace('\n',' ')
    # check that lyrics exist
    if lyrics[:25] == 'We do not have the lyrics':
        return None
    # remove contributor information
    index_contrib = None
    if author_info == True:
        index_contrib = lyrics.rfind('---')
        if index_contrib == -1:
            index_contrib = None
    results['lyrics'] = lyrics[:index_contrib]

    return results
    


if __name__ == '__main__':
    get_lyrics()




