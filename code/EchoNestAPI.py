import json
import pandas as pd
import datetime
import time
import os.path
import requests
from pyechonest import config
from pyechonest import song

timeout_sec = 20  # set timeout parameter for echonest song.search() and requests.get()
config.CALL_TIMEOUT = timeout_sec



def get_API_data(start=0, end=None, input_filename='../data/billboard_tracks.csv'):
    '''
    INPUT: path to billboard data
    OUTPUT: None
    DESC: Calls EchoNest API to get track data
    '''
    df = pd.read_csv(input_filename, sep='|')

    filenames = generate_filenames(df)

    track_info = zip(df.artist_orig.values, df.song_orig.values, filenames)
    # get subset of data for searches
    track_info = track_info[ start : end ]

    # get current time stamp for error log
    tmstmp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d___%H-%M-%S")

    for track_tuple in track_info:
        call_EN_API(track_tuple[0], track_tuple[1], track_tuple[2], tmstmp)


def generate_filenames(df):
    '''
    INPUT: DataFrame
    OUTPUT: list of filenames as strings
    '''
    artist_clean_list = df.artist_clean.values
    song_clean_list = df.song_clean.values

    return ['{0}___{1}'.format(artist, song) for artist, song
                            in zip(artist_clean_list, song_clean_list)]


def call_EN_API(artist, song_name, filename, tmstmp):
    '''
    INPUTS: artist and song search terms
    OUTPUTS: None
    DESC: writes a json file with track information
    '''
    #ipdb.set_trace()

    filepath = '../data/echonest/{0}.json'.format(filename)
    null_filepath = '../data/echonest_null/{0}.json'.format(filename)
    error_filepath = '../data/echonest_null_results/{0}.csv'.format(tmstmp)

    if os.path.exists(filepath):
        return
    if os.path.exists(null_filepath):
        return

    try:
        search_results = song.search(artist=artist, title=song_name, buckets=['song_hotttnesss'])
    except Exception as inst:
        print "Exception: ", inst
        with open('../data/echonest_error_logs/echonest_errors.csv', 'a') as outfile:
            outfile.write(artist + '`' + song_name + '`' + 'Exc 1: ' + str(inst) +
                            '`' + tmstmp + '\n')
        time.sleep(1.0/3.0)
        return

    if search_results == []:
        with open(error_filepath, 'a') as outfile:
            outfile.write(artist + '|' + song_name + '\n')
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
        print "Exception: ", inst
        with open('../data/echonest_error_logs/echonest_errors.csv', 'a') as outfile:
            outfile.write(artist + '`' + song_name + '`' + 'Exc 2: ' + str(inst) +
                            '`' + tmstmp + '\n')
        time.sleep(1.0/3.0)
        return




if __name__ == '__main__':
    get_API_data()
