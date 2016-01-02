import pandas as pd
import numpy as np
import json
import os



def load_lyrics_data(data_dir='../data/lyrics/', output_filename='Lyrics.pkl', start_index=0, end_index=None):
    '''
    INPUTS: Path to data directory, filename for output pickle
    OUTPUTS: None
    DESC: Reads data from json files, writes to dataframe
    '''
    list_lyrics = []

    for f in os.listdir(data_dir)[ start_index : end_index ]:
        if f.endswith('.json'):
            with open(data_dir + f) as f_in:
                json_data = f_in.read()

            # create dict from json, adding filename as a column
            track_lyrics = json.loads(json_data)
            track_lyrics['filename'] = str(f)[:-5]
            list_lyrics.append(track_lyrics)

    # reset index
    df=pd.DataFrame(list_lyrics)

    # pickle dataframe
    df.to_pickle('../data/' + output_filename)



if __name__ == '__main__':
    load_lyrics_data()
