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
    df['song_clean'] = df.song.map(clean_strings).map(fix_song_typos)

    df['filename'] = df.artist_clean + '___' + df.song_clean

    # Note: Use below lines only after refining the way the tracks data are collapsed
    #       To do this, need to update prev_clean_strings to whatever the previous version did
    # # clean artist and song names as I did in the previous round, to create the same filenames I had
    # # I will use the mapping from previous filename to current filename to rename EN and Lyrics files
    # df['prev_artist_clean'] = df.artist.map(prev_clean_strings)
    # df['prev_song_clean'] = df.song.map(prev_clean_strings)
    # df['prev_filename'] = df.prev_artist_clean + '___' + df.prev_song_clean
    # # save old and new filenames to use when cleaning up EN files
    # filenames = df.groupby(['prev_filename']).agg({'filename' : min})
    # filenames.rename(columns={'filename_min': 'filename'}, inplace=True)
    # filenames.reset_index(inplace=True)
    # filenames.to_pickle('../data/filename_conversion.pkl')

    # subset df based on maximum position and first year
    extract_year = (lambda x: x.year)
    df = df[(df.pos <= max_pos) & (df.date.map(extract_year) >= first_year)]

    # create dataframe, collapsed by track
    tracks = create_table(df, ['artist_clean', 'song_clean'])

    # save as csv
    tracks.to_csv(output_filename, sep='|')

    # save pickled dataframe
    tracks.to_pickle('../data/' + pickled_df_name)


# def prev_clean_strings(txt):
#     invalid_punc = '[!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~§]'
#     return re.sub(invalid_punc, '', txt)

def clean_strings(txt):
    invalid_punc = '[!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~§]'
    txt = re.sub(invalid_punc, '', txt)
    # remove 'a', 'the', and extraneous white space
    # check first if txt has more than one word, because there is an artist called "A"
    if len(txt.split()) == 1:
        return ' '.join(txt.split())
    else:
        return ' '.join([word for word in txt.split() if word.lower() not in ['the', 'a']])

def fix_song_typos(txt):
    txt.replace('Livin On Prayer', 'Living On Prayer')
    txt.replace('Im Comin Over', 'Im Coming Over')
    txt.replace('Youre Lookin Good', 'Youre Looking Good')
    txt.replace('Im Livin In Shame', 'Im Living In Shame')
    txt.replace('You Cant Missing Nothing That You Never Had', 'You Cant Miss Nothing That You Never Had')
    txt.replace('Livin It Up', 'Living It Up')
    txt.replace('Feelin Alright', 'Feeling Alright')
    txt.replace('Hold On For Dear Love', 'Holdin On For Dear Love')
    txt.replace('Walking After Midnight', 'Walkin After Midnight')
    txt.replace('Your Bodys Callin', 'Your Bodys Calling')
    txt.replace('Twistin The Night Away', 'Twisting The Night Away')
    txt.replace('Why Im Walkin', 'Why Im Walking')
    txt.replace('These Things Will Keep Me Lovin You', 'These Things Will Keep Me Loving You')
    txt.replace('You Keep Me Hangin On', 'You Keep Me Hanging On')
    txt.replace('Sausilito', 'Sausalito')
    txt.replace('Gorver Henson Feels Forgotten', 'Grover Henson Feels Forgotten')
    txt.replace('Fraulein', 'Freulein')
    txt.replace('Pass The Curvoisier Part II', 'Pass The Courvoisier Part II')
    txt.replace('Stop Look What Your Doing', 'Stop Look What Youre Doing')
    txt.replace('Show Me What Im Loking For', 'Show Me What Im Looking For')
    txt.replace('My Favourite Girl', 'My Favorite Girl')
    txt.replace('YesSireEe', 'YesSirEe')
    txt.replace('Sweet Potatoe Pie', 'Sweet Potato Pie')
    txt.replace('Bonnie Came Back', 'Bonnie Come Back')
    txt.replace('Lonesom', 'Lonesome')
    txt.replace('Cruisng Down The River', 'Cruising Down The River')
    txt.replace('Loosing Your Love', 'Losing Your Love')
    txt.replace('Neighbor Neighbor', 'Neighbour Neighbour')
    txt.replace('Cheryl Moana Marie', 'Cheryl Mona Marie')
    txt.replace('Birthday Suite', 'Birthday Suit')
    txt.replace('Summer Souveniers', 'Summer Souvenirs')
    txt.replace('Never Leave You Uh Oooh Uh Oooh', 'Never Leave You Uh Ooh Uh Oooh')
    txt.replace('Harder To Breath', 'Harder To Breathe')
    txt.replace('More Then You Know', 'More Than You Know')
    txt.replace('Figuered You Out', 'Figured You Out')
    txt.replace('Shake Your Grove Thing', 'Shake Your Groove Thing')
    txt.replace('Ill Be Seing You', 'Ill Be Seeing You')
    txt.replace('Da Ya Think Im Sexy', 'Do Ya Think Im Sexy')
    txt.replace('Ring Dang Do', 'Ring Dang Doo')
    txt.replace('Early Morning Live', 'Early Morning Love')
    txt.replace('I Will Rememeber You', 'I Will Remember You')
    txt.replace('Summer Sweatheart', 'Summer Sweetheart')
    txt.replace('Speedoo', 'Speedo')
    txt.replace('The Angeles Listened In', 'The Angels Listened In')
    txt.replace('Souveniers', 'Souvenirs')
    return txt


def create_table(df, col_list):
    '''
    INPUT: Pandas DataFrame, list of columns to group by
    OUTPUT: Pandas DataFrame
    DESC: Groups original data by artist and song, calculates summary data, and
        sorts by number of weeks in the top "N"
    '''
    grouped = df.groupby(col_list).agg({'pos' : [min, max, tup],
                                        'date' : [min, max, tup],
                                        'count' : sum,
                                        'song' : min,
                                        'artist' : min,
                                        'filename' : min})

    # reset index so that artist and song become columns, and observations are indexed by row number
    grouped = grouped.reset_index()

    # create new names for columns
    multi_index = grouped.columns
    col_names = pd.Index([e[0] + '_' + e[1] if e[1] != '' else e[0] for e in multi_index.tolist()])
    # the below renames and also converts multi-index for columns to one level
    grouped.columns = col_names
    grouped.rename(columns={'count_sum': 'num_wks',
                            'song_min': 'song_orig',
                            'artist_min': 'artist_orig',
                            'filename_min': 'filename'
                            }, inplace=True)

    return grouped.sort_values(by='num_wks', ascending=False)


def tup(x):
    return tuple(x)


if __name__ == '__main__':
    aggregate_by_track()
