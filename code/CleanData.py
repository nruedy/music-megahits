import pandas as pd
import numpy as np



def clean_data(df):
    df.lyrics.fillna('', inplace=True)
    df['lyrics_len'] = df.lyrics.apply(lambda x: len(x))

    # truncate duration to 10 minutes
    df.duration = df.duration.map(lambda x: 600 if x > 600 else x)

    # subset to obs with Echo Nest data
    df_EN = df[df.EN_data == 1]

    # fill in Echo Nest data with missing values
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