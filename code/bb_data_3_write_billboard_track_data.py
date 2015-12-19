import pandas as pd
import datetime
import re



def aggregate_by_track(weekly_data_filename='../data/billboard.csv',
                                      output_filename='../data/billboard_tracks.csv',
                                        pickled_df_name='billboard_tracks.pkl'):
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
    grouped = df.groupby(col_list).agg({'pos' : [min, max],
                                        'date' : [min, max],
                                        'count' : sum,
                                        'song' : min,
                                        'artist' : min})

    new_df = grouped.reset_index()
    new_df.columns = ['artist_clean','song_clean','first_wk','last_wk','num_wks',
                      'artist_orig','min_pos','max_pos','song_orig']
    return new_df.sort('num_wks', ascending=False)


if __name__ == '__main__':
    open('../data/billboard_tracks.csv', 'w').close()
    aggregate_by_track()
