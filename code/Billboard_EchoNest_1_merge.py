import pandas as pd
import bb_data_3_write_billboard_track_data as bb_tracks



def merge_datasets(billboard_pickle='../data/billboard_tracks.pkl',
                   echonest_pickle='../data/EN_features.pkl',
                   output_filename='BB_EN_merged.pkl'):
    '''
    INPUTS: Path to pickled Billboard and EchoNest DataFrames, filename for pickled merged file
    OUTPUTS: None
    DESC: Merges Billboard data with EchoNest features, and pickles resulting dataframe
    '''
    echonest = pd.read_pickle(echonest_pickle)

    billboard = pd.read_pickle(billboard_pickle)
    billboard['merge_column'] = billboard.artist_clean + '___' + billboard.song_clean

    # merge data sets
    df = pd.merge(billboard, echonest,
                  left_on=['merge_column'],
                  right_on=['filename'],
                  how='inner')

    # drop unneeded columns
    df.drop(['merge_column'], inplace=True, axis=1)

    df.to_pickle('../data/' + output_filename)



if __name__ == '__main__':
    # below, change subset position and subset year to change the filtering of the data
    subset_pos = 100
    subset_year = 1955
    # adjust output pickle name accordingly
    billboard_pickle = 'billboard_tracks_pos{0}_yr{1}.pkl'.format(subset_pos, subset_year)

    # run program to collapse filtered billboard data by track, and save as pickled df
    bb_tracks.aggregate_by_track(pickled_df_name=billboard_pickle, max_pos=subset_pos, first_year=subset_year)

    # merge filtered Billboard data with Echo Nest data
    merge_datasets(billboard_pickle='../data/'+billboard_pickle,
                   output_filename='BB_{0}_{1}_EN_merged.pkl'.format(subset_pos, subset_year))
