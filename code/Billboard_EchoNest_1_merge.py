import pandas as pd



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
                  how='outer')

    # drop unneeded columns
    df.drop(['merge_column'], inplace=True, axis=1)

    df.to_pickle('../data/' + output_filename)



if __name__ == '__main__':
    merge_datasets()
