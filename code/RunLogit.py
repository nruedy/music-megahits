import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score



def run_logit_num_wks(df, X_col_names, max_predictors_to_print=None,
                      threshold_high=20, threshold_low=3):
    # create dichotomous target for number of weeks
    df['wks_class'] = df.num_wks.apply(lambda x: wks_bucket(x, threshold_high, threshold_low))
    # select observations that have a target
    df_model = df[df.wks_class.notnull()]
    print 'Counts for target buckets:'
    target_zero_count, target_one_count = df_model.wks_class.value_counts().values
    print 'Number of hits: {0}'.format(target_one_count)
    print 'Number of non-hits: {0}'.format(target_zero_count)
    print ''

    # prepare predictors and target for model by scaling and splitting into test-train sets
    y = df_model.wks_class
    X = df_model[X_col_names]
    X_train, X_test, y_train, y_test = standardize_and_split(X, y)

    lr = LogisticRegression(class_weight='auto')
    lr.fit(X_train, y_train)
    y_prob = lr.predict_proba(X_test)[:, 1]
    auc_ = roc_auc_score(y_test, y_prob)
    print 'Accuracy: ', lr.score(X_test, y_test)
    print 'AUC:', auc_
    print ''

    coef_importance = sorted(zip(X_col_names, list(lr.coef_[0])), key=getKey)

    for coef in coef_importance[: max_predictors_to_print]:
        print '{0}: {1:.3f}'.format(coef[0], coef[1])

    return coef_importance


def wks_bucket(num_wks, threshold_high, threshold_low):
    if num_wks > threshold_high:
        return 1
    elif num_wks < threshold_low:
        return 0
    return None

def standardize_and_split(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    raw_scaler = StandardScaler()
    raw_scaler.fit(X_train)
    X_train = raw_scaler.transform(X_train)
    X_test = raw_scaler.transform(X_test)
    return X_train, X_test, y_train, y_test

def getKey(item):
    return -abs(item[1])


def subset_by_year(df, from_year, to_year):
    return df[(df.date_min.apply(lambda x: x.year) >= from_year) & (df.date_min.apply(lambda x: x.year) <= to_year)]


'''
X = df[['energy', 'liveness', 'tempo', 'mode', 'acousticness', 'instrumentalness', \
       'danceability', 'duration', 'loudness', 'valence', 'speechiness', \
       'bars_confidence_mean', 'bars_confidence_sd', 'bars_duration_sd', \
       'beats_confidence_mean', 'beats_confidence_sd', 'beats_duration_mean', \
        'beats_duration_sd', 'num_keys', 'num_sections', 'segment_loudness_sd', \
        'tatums_confidence_mean', 'tatums_confidence_sd', 'tatums_duration_sd', \
        'timbre_01_mean', 'timbre_01_sd', 'timbre_02_mean', 'timbre_02_sd', \
        'timbre_03_mean', 'timbre_03_sd', 'timbre_04_mean', 'timbre_04_sd', \
        'timbre_05_mean', 'timbre_05_sd', 'timbre_06_mean', 'timbre_06_sd', \
        'timbre_07_mean', 'timbre_07_sd', 'timbre_08_mean', 'timbre_08_sd', \
        'timbre_09_mean', 'timbre_09_sd', 'timbre_10_mean', 'timbre_10_sd', \
        'timbre_11_mean', 'timbre_11_sd', 'timbre_12_mean', 'timbre_12_sd', \
        'song_type_acoustic', 'song_type_childrens', 'song_type_christmas', \
        'song_type_electric', 'song_type_instrumental', 'song_type_karaoke', \
        'song_type_live', 'song_type_remix', 'song_type_studio', u'song_type_tribute', \
        'song_type_vocal', 'key_C', 'key_Cs','key_D','key_Ds','key_E',
        'key_F', 'key_Fs','key_G', 'key_Gs', 'key_A', 'key_As',
        'time_sig_4', 'time_sig_3',]]
'''