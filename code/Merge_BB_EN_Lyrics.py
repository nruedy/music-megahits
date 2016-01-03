import pandas as pd
import Billboard_3_write_track_data as BB_3



def merge_datasets(billboard_pickle='../data/billboard_tracks.pkl',
                   echonest_pickle='../data/EN_features.pkl',
                   lyrics_pickle='../data/Lyrics.pkl',
                   output_filename='BB_EN_L_merged.pkl'):
    '''
    INPUTS: Path to pickled Billboard and EchoNest DataFrames, filename for pickled merged file
    OUTPUTS: None
    DESC: Merges Billboard data with EchoNest features, and pickles resulting dataframe
    '''
    echonest = pd.read_pickle(echonest_pickle)
    # create dummy to use to indicate if there is EN data for a given record
    echonest['EN_data'] = 1

    billboard = pd.read_pickle(billboard_pickle)
    #billboard['merge_column'] = billboard.artist_clean + '___' + billboard.song_clean

    # merge data BB and EN data sets
    df = pd.merge(billboard, echonest,
                  left_on=['filename'],
                  right_on=['filename'],
                  how='left')

    # add lyrics
    lyrics = pd.read_pickle(lyrics_pickle)
    # create dummy to use to indicate if there are Lyrics for a given record
    lyrics['L_data'] = 1

    df = pd.merge(df, lyrics,
                  left_on=['filename'],
                  right_on=['filename'],
                  how='left')


    df.to_pickle('../data/' + output_filename)



if __name__ == '__main__':
    # below, change subset position and subset year to change the filtering of the data
    subset_pos = 100
    subset_year = 1955
    # adjust output pickle name accordingly
    billboard_pickle = 'billboard_tracks_pos{0}_yr{1}.pkl'.format(subset_pos, subset_year)

    # run program to collapse filtered billboard data by track, and save as pickled df
    BB_3.aggregate_by_track(pickled_df_name=billboard_pickle, max_pos=subset_pos, first_year=subset_year)

    # merge filtered Billboard data with Echo Nest data
    merge_datasets(billboard_pickle='../data/'+billboard_pickle,
                   output_filename='BB_{0}_{1}_EN_L_merged.pkl'.format(subset_pos, subset_year))
