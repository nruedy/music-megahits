# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import re



# set path for input data
weekly_data_filename='../data/billboard.csv'
output_filename='../data/billboard_tracks.csv'


# TODO: refactor code so that if max_pos or first_year are None, no filtering occurs on that field
def aggregate_by_track(pickled_df_name='billboard_tracks.pkl', max_pos=200, first_year=1930):
    '''
    INPUT: billboard data at the weekly level (week, artist, song, position)
    OUTPUT: data file aggregated by track (i.e., song/artist combination), and pickled dataframe
    '''
    # read in week-level data
    df = pd.read_csv(weekly_data_filename, sep='|', names=['date','pos','song','artist'])

    # get rid of rows with artist and song = '-'
    df = df[(df.song != '-') & (df.artist != '-')]

    # convert dates from strings to datetime objects
    convert_to_date = (lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date())
    df.date = df.date.map(convert_to_date)

    # adding column of 1's, in order to sum them later for counts
    df['count'] = 1

    # clean artist and song names, before using them to collapse data
    df['artist_clean'] = df.artist.map(clean_strings)
    df['song_clean'] = df.song.map(clean_strings)

    # subset df based on maximum position and first year
    extract_year = (lambda x: x.year)
    df = df[(df.pos <= max_pos) & (df.date.map(extract_year) >= first_year)]

    # create dataframe, collapsed by track
    tracks = create_table(df, ['artist_clean', 'song_clean'])

    # save as csv
    tracks.to_csv(output_filename, sep='|')

    # save pickled dataframe
    tracks.to_pickle('../data/' + pickled_df_name)


def clean_strings(txt):
    invalid_punc = '[!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~§]'
    return re.sub(invalid_punc, '', txt)


def create_table(df, col_list):
    '''
    INPUT: Pandas DataFrame, list of columns to group by
    OUTPUT: Pandas DataFrame
    DESC: Groups origingal data by artist and song, calculates summary data, and
        sorts by number of weeks in the top "N"
    '''
    grouped = df.groupby(col_list).agg({'pos' : [min, max, tup],
                                        'date' : [min, max, tup],
                                        'count' : sum,
                                        'song' : min,
                                        'artist' : min})

    # reset index so that artist and song become columns, and observations are indexed by row number
    grouped = grouped.reset_index()

    # create new names for columns
    multi_index = grouped.columns
    col_names = pd.Index([e[0] + '_' + e[1] if e[1] != '' else e[0] for e in multi_index.tolist()])
    # the below renames and also converts multi-index for columns to one level
    grouped.columns = col_names
    grouped.rename(columns={'count_sum': 'num_wks', 'song_min': 'song_orig', 'artist_min': 'artist_orig'}, inplace=True)

    return grouped.sort_values(by='num_wks', ascending=False)


def tup(x):
    return tuple(x)


if __name__ == '__main__':
    aggregate_by_track()
