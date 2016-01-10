import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.ensemble.partial_dependence import plot_partial_dependence


# Note: Models are run in 'ML Models' notebook


def prep_data(df, X_col_names, scaled=False, threshold_high=20, threshold_low=6):
    '''
    INPUTS: DataFrame, List of feature names, Bool (Indicate scaling), Int (Threshold for hit),
    Int (Threshold for non-hit)
    OUTPUTS: Four Arrays
    DESC: Produces testing and training features and labels
    '''
    df_model = df
    # create dichotomous target for number of weeks
    df_model['wks_class'] = df_model.num_wks.apply(lambda x: wks_bucket(x, threshold_high, threshold_low))
    # select observations that have a target
    df_model = df[df.wks_class.notnull()]
    print 'Counts for target buckets:'
    target_one_count = len(df_model[df_model.wks_class==1].index)
    target_zero_count = len(df_model[df_model.wks_class==0].index)
    print 'Number of hits: {0}'.format(target_one_count)
    print 'Number of non-hits: {0}'.format(target_zero_count)
    print ''

    # prepare predictors and target for model by scaling and splitting into test-train sets
    y = df_model.wks_class
    X = df_model[X_col_names]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    if scaled == True:
        X_train, X_test = scale_data(X_train, X_test)
    return X_train, X_test, y_train, y_test


def scale_data(X_train, X_test):
    '''
    INPUTS: Matrix, Matrix
    OUTPUTS: Matrix, Matrix
    DESC: Scales train and test data sets based on train set
    '''
    raw_scaler = StandardScaler()
    raw_scaler.fit(X_train)
    X_train = raw_scaler.transform(X_train)
    X_test = raw_scaler.transform(X_test)
    return X_train, X_test


def run_model(clf, X_train, X_test, y_train, y_test):
    '''
    :param clf: classifier
    :param X_train: Matrix (features)
    :param X_test: Matrix (features)
    :param y_train: Matrix (labels)
    :param y_test: Matrix (labels
    :return: array (predicted probabilities)
    '''
    clf.fit(X_train, y_train)
    y_prob = clf.predict_proba(X_test)[:, 1]
    auc_ = roc_auc_score(y_test, y_prob)
    print 'Accuracy: ', clf.score(X_test, y_test)
    print 'AUC:', auc_
    return y_prob


def logit_results(clf, X_col_names, max_predictors_to_print=None):
    '''
    :param clf: Classifier
    :param X_col_names: List of feature names
    :param max_predictors_to_print: Number of predictors to list in output
    :return: Coefficient importances
    '''

    coef_importance = sorted(zip(X_col_names, list(clf.coef_[0])), key=getKey)

    print 'Top predictors:'
    for coef in coef_importance[: max_predictors_to_print]:
        print '{0}: {1:.3f}'.format(coef[0], coef[1])

    return coef_importance


def grad_boost_classifier_results(clf, X_train, X_col_names, num_top_features=10):
    '''
    :param clf: Classifier
    :param X_train: Matrix
    :param X_col_names: List of feature names
    :param num_top_features: Number of features for which to pring output
    :return:
    '''
    importances = pd.Series(clf.feature_importances_, index=X_col_names)
    importances.sort(ascending=False)

    top_feat_import = importances.head(num_top_features).index.values
    top_feat_import_indices = [list(X_col_names).index(feat) for feat in top_feat_import]

    fig,axs = plot_partial_dependence(clf, X_train, top_feat_import_indices, feature_names=X_col_names)
    fig.set_size_inches(10,3.25 * (num_top_features/3 + (1 if num_top_features % 3 > 0 else 0)))
    return importances


def wks_bucket(num_wks, threshold_high, threshold_low):
    '''
    :param num_wks: Number of weeks song was in the Billboard Chart
    :param threshold_high: Threshold for long-running song
    :param threshold_low: Threshold for a short-running song
    :return: label value
    '''
    if num_wks > threshold_high:
        return 1
    elif num_wks < threshold_low:
        return 0
    return None


def getKey(item):
    '''
    :param item: tuple of feature name and feature importance
    :return: key to sort by
    '''
    return -abs(item[1])




