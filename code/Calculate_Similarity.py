import pandas as pd
import numpy as np


def sim_calc(df, colnames_list):
    '''
    INPUTS: DataFrame (data merged from BB and EN), list of column names
    OUTPUTS: DataFrame of similarities, which can be concatenated with original DataFrame
    DESC: For each row in df, finds the tracks which occupied the Billboard for at least one
    overlapping week. For these tracks, calculates the mean and SD of the features
    (which correspond to colnames_list) in order to normalize the track's feature value to the
    number of SDs above or below the mean it was, relative to songs that were popular around
    the same time.
    '''
    new_df = pd.DataFrame(index=range(len(df)), columns=['sim_' + colname for colname in colnames_list])
    for row in list(df.index):
        #create dataframe where there is an overlap between min week and max week with target
        cohort_indices = df.date_tup.apply(lambda x: len(set(df.date_tup[row]) & set(x)) != 0)
        cohort_indices = list(cohort_indices.values)
        # mask columns by indices to get comparison data
        comparison_data = df.ix[cohort_indices, colnames_list]
        for i, colname in enumerate(colnames_list):
            if df.ix[row, colname] != None:
                new_df.ix[row, 'sim_' + colname] = (df.ix[row, colname] - np.mean(comparison_data.ix[:, i])) \
                                                   / np.std(comparison_data.ix[:, i])
        if row % 10 == 0:
            print '{0} records processed'.format(row)
    pd.to_pickle(new_df, '../data/BB_100_1955_EN_merged_sim.pkl')


if __name__ == '__main__':
    input_data = '../data/BB_100_1955_EN_merged.pkl'
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

    df_sim = sim_calc(df, col_list)
