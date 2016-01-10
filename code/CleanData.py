import pandas as pd
import numpy as np



def clean_data(df):
    '''
    :param df: DataFrame
    :return:
    '''
    df.lyrics.fillna('', inplace=True)
    df['lyrics_len'] = df.lyrics.apply(lambda x: len(x))

    # remove songs that are outside the range of 90 sec and 10 min
    df = df[(df.duration <= 600) & (df.duration >= 90)]

    # subset to obs with Echo Nest data
    df_EN = df[df.EN_data == 1]

    # fill in Echo Nest data with missing values
    # (There are ~20 or fewer missing values per feature)
    cols_with_missing = ['instrumentalness', 'speechiness', 'bars_confidence_mean', 'bars_confidence_sd',
                         'bars_duration_sd', 'beats_confidence_mean', 'beats_confidence_sd', 'beats_duration_mean',
                         'beats_duration_sd', 'tatums_confidence_mean', 'tatums_confidence_sd', 'tatums_duration_sd',
                         'sim_instrumentalness', 'sim_speechiness', 'sim_bars_confidence_mean', 'sim_bars_confidence_sd',
                         'sim_bars_duration_sd', 'sim_beats_confidence_mean', 'sim_beats_confidence_sd', 'sim_beats_duration_mean',
                         'sim_beats_duration_sd', 'sim_tatums_confidence_mean', 'sim_tatums_confidence_sd', 'sim_tatums_duration_sd',
                         ]
    for col in cols_with_missing:
        if col in list(df_EN.columns):
            df_EN[col] = df_EN[col].fillna(df[col].mean())

    return df_EN


def print_counts(df):
    '''
    :param df: DataFrame
    :return: None
    '''
    N_obs, N_cols = df.shape
    N_EN, _ = df[df.EN_data == 1].shape

    print 'Number of obs:      {0:>6d}'.format(N_obs)
    print 'Number with EN:     {0:>6d}  {1:.1f}%'.format(N_EN, 100 * N_EN / float(N_obs))


def subset_by_year(df, from_year, to_year):
    '''
    :param df: DataFrame
    :param from_year: Integer
    :param to_year: Integer
    :return: DataFrame
    '''
    return df[(df.date_min.apply(lambda x: x.year) >= from_year) & (df.date_min.apply(lambda x: x.year) <= to_year)]


def select_features():
    '''
    :return: List of features for modelling
    '''
    X_cols_full = ['energy', 'liveness', 'tempo', 'mode', 'acousticness', 'instrumentalness',
       'danceability', 'duration', 'loudness', 'valence', 'speechiness',
       'bars_confidence_mean', 'bars_confidence_sd', 'bars_duration_sd',
       'beats_confidence_mean', 'beats_confidence_sd', 'beats_duration_mean',
        'beats_duration_sd', 'num_keys', 'num_sections', 'segment_loudness_sd',
        'tatums_confidence_mean', 'tatums_confidence_sd', 'tatums_duration_sd',
        'timbre_01_mean', 'timbre_01_sd', 'timbre_02_mean', 'timbre_02_sd',
        'timbre_03_mean', 'timbre_03_sd', 'timbre_04_mean', 'timbre_04_sd',
        'timbre_05_mean', 'timbre_05_sd', 'timbre_06_mean', 'timbre_06_sd',
        'timbre_07_mean', 'timbre_07_sd', 'timbre_08_mean', 'timbre_08_sd',
        'timbre_09_mean', 'timbre_09_sd', 'timbre_10_mean', 'timbre_10_sd',
        'timbre_11_mean', 'timbre_11_sd', 'timbre_12_mean', 'timbre_12_sd',
        'song_type_acoustic', 'song_type_childrens', 'song_type_christmas',
        'song_type_electric', 'song_type_instrumental', 'song_type_karaoke',
        'song_type_live', 'song_type_remix', 'song_type_studio', 'song_type_tribute',
        'song_type_vocal', 'key_C', 'key_Cs','key_D','key_Ds','key_E',
        'key_F', 'key_Fs','key_G', 'key_Gs', 'key_A', 'key_As',
        'time_sig_4', 'time_sig_3',]

    X_cols_sim_full = [u'sim_energy', u'sim_liveness', u'sim_tempo', u'sim_mode',
       u'sim_acousticness', u'sim_instrumentalness', u'sim_danceability',
       u'sim_duration', u'sim_loudness', u'sim_valence', u'sim_speechiness',
       u'sim_bars_confidence_mean', u'sim_bars_confidence_sd',
       u'sim_bars_duration_sd', u'sim_beats_confidence_mean',
       u'sim_beats_confidence_sd', u'sim_beats_duration_mean',
       u'sim_beats_duration_sd', u'sim_num_keys', u'sim_num_sections',
       u'sim_segment_loudness_sd', u'sim_tatums_confidence_mean',
       u'sim_tatums_confidence_sd', u'sim_tatums_duration_sd',
       u'sim_timbre_01_mean', u'sim_timbre_01_sd', u'sim_timbre_02_mean',
       u'sim_timbre_02_sd', u'sim_timbre_03_mean', u'sim_timbre_03_sd',
       u'sim_timbre_04_mean', u'sim_timbre_04_sd', u'sim_timbre_05_mean',
       u'sim_timbre_05_sd', u'sim_timbre_06_mean', u'sim_timbre_06_sd',
       u'sim_timbre_07_mean', u'sim_timbre_07_sd', u'sim_timbre_08_mean',
       u'sim_timbre_08_sd', u'sim_timbre_09_mean', u'sim_timbre_09_sd',
       u'sim_timbre_10_mean', u'sim_timbre_10_sd', u'sim_timbre_11_mean',
       u'sim_timbre_11_sd', u'sim_timbre_12_mean', u'sim_timbre_12_sd']


    # removing num_keys and sim_num_keys (about 4000 values are equal to zero)
    # removing sim_mode because mode is dichotomous
    X_cols_to_remove = ['num_keys', 'sim_num_keys', 'sim_mode']
    return [col for col in X_cols_full + X_cols_sim_full if col not in X_cols_to_remove]
