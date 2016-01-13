'''
This script provides an outline for the all the code that collects, cleans, and
prepares data for analysis.

Approximate run times are provided in comments.
'''


import Billboard_1_scrape as BB_1
import Billboard_2_write_weekly_data as BB_2
import Billboard_3_write_track_data as BB_3
import Update_EN_Lyrics_with_revised_filenames as Update_EN_L
import EchoNest_1_call_API as EN_1
import EchoNest_2_read_data as EN_2
import Lyrics_1_scrape as L_1
import Lyrics_2_write_data as L_2
import Merge_BB_EN_Lyrics as BB_EN_L
import Calculate_Similarity as CalcSim



if __name__ == '__main__':

    ### BILLBOARD DATA ###

    '''
    Scrape Billboard data to find the position, artist, and song for each week
    Time: 1 minute, or several hours if starting from scratch

    Note: To update with latest data, set first_date to the first week of missing data,
    and last_date to the date of last available data.
    The program adds text files for each new week -- no need to re-scape previous weeks.
    '''
    BB_1.get_content_from_urls(first_date='2015-12-12', last_date='2016-1-02')


    '''
    Write Billboard data to one CSV file.
    Time: < 1 minute

    Note: The script appends to the file, so the line below erases the file contents,
    avoiding duplicates.
    '''
    open('../data/billboard.csv', 'w').close()
    BB_2.write_billboard_data('../data/billboard.csv')


    '''
    Aggregate Billboard data by track
    Time: < 1 minute

    This file collapses the Billboard data based on a unique song & artist combination
    It cleans/standardizes the strings for artist and song first. This is important,
    because otherwise one song would have two separate entries in the data, and the
    number of weeks that song was in the charts would be divided between those two entries.

    Each unique song-artist combination is used as a filename in later scripts which
    scrape for Echo Nest data and song lyrics. In case cleaning of the Billboard data
    takes place after these filenames have been created, this file provides a mechanism
    to update the previous filenames with the new ones, and delete any duplicates.
    '''
    # Commented out because merge code runs taking the desired subset, so this
    # is redundant
    # BB_3.aggregate_by_track(pickled_df_name='billboard_tracks.pkl')

    # Commented out because they only need to run if track data has been revised
    # Update_EN_L.rename_files_after_track_revisions(directory_path = '../data/echonest/')
    # Update_EN_L.rename_files_after_track_revisions(directory_path = '../data/lyrics/')


    ### ECHO NEST DATA ###

    '''
    Call Echo Nest API
    Time: Several hours

    Calls Echo Nest API for each track and saves audio data for each as a .json file.
    Tries several different ways of searching on artist and song, because the
    match-up is imperfect. Currently at 84% matching.
    '''
    EN_1.get_API_data(start=0, end=None, input_filename='../data/billboard_tracks.pkl')


    '''
    Write Echo Nest data to DataFrame (pickled)
    Time: 60 min

    Pulls out the desired features from the Echo Nest .json files, and performs feature
    engineering (e.g., calculating the variance for bar duration, and creating dummies
    for key).
    '''
    EN_2.load_data(data_dir='../data/echonest/', output_filename='EN_features.pkl')


    ### LYRICS ###

    '''
    Scrape Lyrics
    Time: 1-3 hours

    Searches SongLyrics.com, and then Lyrics.com based on artist and song. Tries several
    different searches, because the match-up is imperfect.
    '''
    L_1.get_lyrics(start=0, end=None, input_filename='../data/billboard_tracks.pkl')


    '''
    Write Lyrics Data
    Time: 5-10 seconds

    Reads lyrics data from .json files, and writes to a DataFrame (pickled).

    #TODO: Data cleaning could happen here, before writing.
    '''
    L_2.load_lyrics_data(data_dir='../data/lyrics/', output_filename='Lyrics.pkl', start_index=0, end_index=None)


    ### MERGE DATASETS ###

    '''
    Merge BB, EN, and Lyrics data
    Time: 90 seconds

    Takes a subset of Billboard data (e.g., year >= 1955, position <= 100), and then aggregates the original
    weekly data into a dataframe with one row for each track. Then, performs a left merge with Echo Nest
    and Lyrics data, such that all Billboard data is retained, but only matching EN and Lyrics data are
    pulled in. For both data sets, before merging, a dummy is created that is equal to 1 if the data exists.
    This is intended to be used to, for instance, only fill in missing values for those that have EN data.
    '''
    # below, change subset position and subset year to change the filtering of the data
    subset_pos = 100
    subset_year = 1955
    # adjust output pickle name accordingly
    billboard_pickle = 'billboard_tracks_pos{0}_yr{1}.pkl'.format(subset_pos, subset_year)

    # run program to collapse filtered billboard data by track, and save as pickled df
    BB_3.aggregate_by_track(pickled_df_name=billboard_pickle, max_pos=subset_pos, first_year=subset_year)

    # merge filtered Billboard data with Echo Nest data
    BB_EN_L.merge_datasets(billboard_pickle='../data/'+billboard_pickle,
                           echonest_pickle='../data/EN_features.pkl',
                           lyrics_pickle='../data/Lyrics.pkl',
                           output_filename='BB_{0}_{1}_EN_L_merged.pkl'.format(subset_pos, subset_year))


    ### SIMILARITY CALCULATION ###
    '''
    Calculates normalized
    Time: 3-4 hours

    For each row in df, finds the tracks which occupied the Billboard for at least one
    overlapping week. For these tracks, calculates the mean and SD of the features
    (which correspond to colnames_list) in order to normalize the track's feature value to the
    number of SDs above or below the mean it was, relative to songs that were popular around
    the same time.
    '''
    input_data = '../data/BB_100_1955_EN_L_merged.pkl'
    df = pd.read_pickle(input_data)

    col_list = ['energy',
         'liveness',
         'tempo',
         'mode',
         'acousticness',
         'instrumentalness',
         'danceability',
         'duration',
         'loudness',
         'valence',
         'speechiness',
         'bars_confidence_mean',
         'bars_confidence_sd',
         'bars_duration_sd',
         'beats_confidence_mean',
         'beats_confidence_sd',
         'beats_duration_mean',
         'beats_duration_sd',
         'num_keys',
         'num_sections',
         'segment_loudness_sd',
         'tatums_confidence_mean',
         'tatums_confidence_sd',
         'tatums_duration_sd',
         'timbre_01_mean',
         'timbre_01_sd',
         'timbre_02_mean',
         'timbre_02_sd',
         'timbre_03_mean',
         'timbre_03_sd',
         'timbre_04_mean',
         'timbre_04_sd',
         'timbre_05_mean',
         'timbre_05_sd',
         'timbre_06_mean',
         'timbre_06_sd',
         'timbre_07_mean',
         'timbre_07_sd',
         'timbre_08_mean',
         'timbre_08_sd',
         'timbre_09_mean',
         'timbre_09_sd',
         'timbre_10_mean',
         'timbre_10_sd',
         'timbre_11_mean',
         'timbre_11_sd',
         'timbre_12_mean',
         'timbre_12_sd']

    df_sim = CalcSim.sim_calc(df, col_list)


    ### MODELLING ###

    '''
    'ML Models.ipynb' runs the three ML models, using code in modules RunModel.py and CleanData.py
    '''