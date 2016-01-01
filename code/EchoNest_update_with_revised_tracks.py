import pandas as pd
import os



def rename_EN_files():
    filenames = pd.read_pickle('../data/filename_conversion.pkl')
    filenames_diff = filenames[filenames.prev_filename != filenames.filename]

    for file_tup in zip(list(filenames_diff.prev_filename), list(filenames_diff.filename)):
        filepath_from = '../data/echonest/' + file_tup[0] + '.json'
        filepath_to = '../data/echonest/' + file_tup[1] + '.json'

        if os.path.exists(filepath_to):
            if os.path.exists(filepath_from):
                os.remove(filepath_from)
            continue
        if os.path.exists(filepath_from):
            os.rename(filepath_from, filepath_to)



if __name__ == '__main__':
    rename_EN_files()
