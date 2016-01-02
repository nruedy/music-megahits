import pandas as pd
import os


# Note: filename_conversion.pkl gets updated in Billboard_3_write_track_data.py
filenames_pickle_path = '../data/filename_conversion.pkl'


def rename_files_after_track_revisions(directory_path):
    '''
    INPUTS: string (directory_path -- gives path to directory where files should be changed)
    OUTPUTS: None
    DESC: Renames files with updated filenames after tracks have been consolidated
    '''
    filenames = pd.read_pickle(filenames_pickle_path)
    filenames_diff = filenames[filenames.prev_filename != filenames.filename]

    for file_tup in zip(list(filenames_diff.prev_filename), list(filenames_diff.filename)):
        filepath_from = directory_path + file_tup[0] + '.json'
        filepath_to = directory_path + file_tup[1] + '.json'

        if os.path.exists(filepath_to):
            if os.path.exists(filepath_from):
                os.remove(filepath_from)
            continue
        if os.path.exists(filepath_from):
            os.rename(filepath_from, filepath_to)



if __name__ == '__main__':
    rename_files_after_track_revisions(directory_path = '../data/echonest/')
    rename_files_after_track_revisions(directory_path = '../data/lyrics/')