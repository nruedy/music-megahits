'''
Reads Echo Nest features from JSON files and saves as pickled dataframe.
'''


import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
from timeit import default_timer as timer


# TODO: Refactor for efficiency - perhaps write to a dict instead of a dataframe.
def load_data(data_dir='../data/echonest/', output_filename='EN_features.pkl', start_index=0, end_index=None):
    '''
    Pickles dataframe

    INPUTS: Path to data directory, filename for output pickle
    OUTPUTS: None
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
            cols_to_drop = ['analysis_url', 'audio_md5', 'meta', 'track']
            df_row.drop(cols_to_drop, axis=1, inplace=True)

            #### loop through lists in 'bars', 'beats' and 'tatums' and save desired data

            for analysis_level in ['bars', 'beats', 'tatums']:
                df_row = calc_list_stats(df_row, analysis_level)

            #### add section data

            section_data = dict()
            # transform sections (list of dicts) into a dict of lists
            dict_section_stats = transform_dicts(df_row.sections[0])
            # count number of sections
            section_data['num_sections'] = len(df_row.sections[0])
            # add sd for tempo and loudness
            for colname in ['tempo', 'loudness']:
                section_data['section_' + colname + '_sd'] = np.std(dict_section_stats[colname])

            # major = 0; minor = 1
            # keys {0: 'C', 1: 'Cs', 2: 'D', 3: 'Ds', 4: 'E', 5: 'F', 6: 'Fs', 7: 'G', 8: 'Gs', 9: 'A', 10: 'As', 11: 'B'}
            distinct_keys = set()
            for key_mode in zip(dict_section_stats['key'],dict_section_stats['mode']):
                if key_mode[1]==0:
                    distinct_keys.add(key_mode[0])
                else:
                    distinct_keys.add((key_mode[0] + 3) % 12)

            section_data['num_keys']=len(distinct_keys)

            section_data_df = pd.DataFrame.from_dict([section_data])
            df_row = pd.concat([df_row, section_data_df], axis=1)
            df_row.drop('sections', inplace=True, axis=1)

            #### add segment data

            segment_data = dict()
            # transform segments (list of dicts) into a dict of lists
            dict_segment_stats = transform_dicts(df_row.segments[0])

            # add sd for loudness
            segment_data['segment_loudness_sd'] = np.std(dict_segment_stats['loudness_max'])

            # timbre - transpose segment lists so that there are 12 lists - one for each timbre
            '''
            Timbres are high level abstractions of the spectral surface, ordered by degree
            of importance. For completeness, the first dimension represents the average
            loudness of the segment; second emphasizes brightness; third is more closely
            correlated to the flatness of a sound; fourth to sounds with a stronger attack; etc.
            '''
            timbre_list = np.asarray(dict_segment_stats['timbre']).T.tolist()
            timbre_count = 1
            for timbre in timbre_list:
                segment_data['timbre_{0:02d}_mean'.format(timbre_count)] = np.mean(timbre)
                segment_data['timbre_{0:02d}_sd'.format(timbre_count)] = np.std(timbre)
                timbre_count += 1

            segment_data_df = pd.DataFrame.from_dict([segment_data])
            df_row = pd.concat([df_row, segment_data_df], axis=1)
            df_row.drop('segments', inplace=True, axis=1)


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

    # keys: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
    # leaving out 'B' to have n-1 dummies
    keys_dict = {0: 'C', 1: 'Cs', 2: 'D', 3: 'Ds', 4: 'E', 5: 'F',
                 6: 'Fs', 7: 'G', 8: 'Gs', 9: 'A', 10: 'As'}

    for k, v in keys_dict.iteritems():
        df['key_' + v] = df.key == k

    #create dummies for time signatures
    df['time_sig_4'] = df.time_signature == 4
    df['time_sig_3'] = df.time_signature == 3
    df['time_sig_1'] = df.time_signature == 1
    df['time_sig_5'] = df.time_signature == 5
    df['time_sig_7'] = df.time_signature == 7

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
