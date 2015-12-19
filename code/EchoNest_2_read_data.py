import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
from timeit import default_timer as timer


def load_data(data_dir='../data/echonest/', output_filename='EN_features.pkl', start_index=0, end_index=None):
    '''
    INPUTS: Path to data directory, filename for output pickle
    OUTPUTS: None
    DESC: Pickles dataframe
    '''
    start_time = timer()
    df = pd.DataFrame()

    count = 0
    for f in os.listdir(data_dir)[ start_index : end_index ]:
        if f.endswith('.json'):
            with open(data_dir + f) as f_in:
                json_data = f_in.read()

            # create dataframe from json, adding filename as a column
            data = json.loads(json_data)
            data['filename'] = str(f)[:-5]
            df_row = pd.DataFrame([data], index=[0])

            # explode first level of dictionaries into columns
            df_row = explode_dicts(df_row)

            # drop unneeded columns
            # NOTE: doing this after exploding the first level of dicts allows
            # dropping second-level data, such as 'meta'
            # TODO: Get segment, section, and track data
            cols_to_drop = ['analysis_url', 'audio_md5', 'meta', 'segments', 'sections', 'track']
            df_row.drop(cols_to_drop, axis=1, inplace=True)

            # loop through lists in 'bars', 'beats' and 'tatums' and save desired data
            for analysis_level in ['bars', 'beats', 'tatums']:
                df_row = calc_list_stats(df_row, analysis_level)

            df = df.append(df_row)

        count += 1
        if count % 100 == 0:
             print '{0} records processed'.format(count)

    # reset index
    df=df.reset_index(drop=True)

    # create song type dummies
    df_song_type = df['song_type'].str.join(sep='*').str.get_dummies(sep='*')
    df_song_type.rename(columns = lambda x : 'song_type_' + x, inplace=True)
    df = pd.concat([df, df_song_type], axis=1)

    # pickle dataframe
    df.to_pickle('../data/' + output_filename)

    # print runtime
    end_time = timer()
    print 'run_time: {0}s'.format(end_time - start_time)


def explode_dicts(df_row):
    '''
    INPUTS: DataFrame
    OUTPUTS: DataFrame
    DESC: Take a df of one observation, and expands the columns that contain dictionaries
    '''
    df_expand = df_row

    for col in df_row.columns:
        col_data = df_row[col][0]
        if type(col_data) == dict:
            new_cols = pd.DataFrame.from_dict([col_data])
            df_expand = pd.concat([df_expand, new_cols], axis=1)
            df_expand.drop(col, inplace=True, axis=1)
    return df_expand


def calc_list_stats(df_row, analysis_level):
    '''
    INPUTS: DataFrame, string (column name)
    OUTPUTS: None
    DESC: Take a df of one observation, and calculates stats on the named column,
    saves the stats in new columns, and deletes the original column
    '''
    list_of_dicts = df_row[analysis_level][0]
    # create empty dict to hold new column values
    new_cols = dict()
    new_cols[analysis_level + '_count'] = len(list_of_dicts)
    dict_stats = transform_dicts(list_of_dicts)
    extract_stats(analysis_level, new_cols, dict_stats, 'duration')
    extract_stats(analysis_level, new_cols, dict_stats, 'confidence')
    new_cols_df = pd.DataFrame.from_dict([new_cols])
    df_expand = pd.concat([df_row, new_cols_df], axis=1)
    df_expand.drop(analysis_level, inplace=True, axis=1)
    return df_expand


def transform_dicts(list_of_dicts):
    '''
    INPUTS: list
    OUTPUTS: dict
    DESC: transforms list of dicts into a dict of lists (by key)
    '''
    d = defaultdict(list)

    #loop through list
    for item in list_of_dicts:
        #loop through the dict to get key, and append value to list:
        for k, v in item.iteritems():
            d[k].append(v)

    return d


def extract_stats(analysis_level, new_cols, dict_stats, colname):
    '''
    INPUTS: string (level of music analysis), dict (to store data), dict (containing stats),
        string (for output column name)
    OUTPUTS: None
    DESC: calculates stats and saves as new columns in new_cols dict
    '''
    stats_list = dict_stats[colname]
    new_cols[analysis_level + '_' + colname + '_mean'] = np.mean(stats_list)
    new_cols[analysis_level + '_' + colname + '_sd'] = np.std(stats_list)


if __name__ == '__main__':
    load_data(data_dir='../data/echonest/', output_filename='EN_features.pkl')
