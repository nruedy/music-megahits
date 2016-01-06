import pandas as pd
import numpy as np



def load_data(pickle_path = '../data/BB_100_1955_EN_L_merged.pkl'):
    return pd.read_pickle(pickle_path)

def print_counts(df):
    N_obs, N_cols = df.shape
    N_EN, _ = df[df.EN_data == 1].shape
    N_L, _ = df[df.L_data == 1].shape
    N_ENL, _ = df[(df.EN_data == 1) & (df.L_data == 1)].shape

    print 'Number of obs:      {0:>6d}'.format(N_obs)
    print 'Number with EN:     {0:>6d}  {1:.1f}%'.format(N_EN, 100 * N_EN / float(N_obs))
    print 'Number with Lyrics: {0:>6d}  {1:.1f}%'.format(N_L, 100 * N_L / float(N_obs))
    print 'Number with Both:   {0:>6d}  {1:.1f}%'.format(N_ENL, 100 * N_ENL / float(N_obs))
    print ''
    print 'Number of cols: {0}'.format(N_cols)


# df.num_wks.hist(bins=87)
# plt.xlabel('Number of Weeks on Top 100 Billboard Chart')
# plt.ylabel('Count')
# plt.show()

# #examing missing Echo Nest data
# df_EN = df[df.EN_data==1]
# X_EN = X[df.EN_data==1]
# X_EN.apply(lambda x: np.sum(pd.isnull(x)))


#if __name__ == '__main__':
    # read in the data and print basic stats
    # df = load_data()
    # print_counts(df)

