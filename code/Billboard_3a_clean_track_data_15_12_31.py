# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import re



def clean_artist(txt):
    return clean_strings(txt)


def clean_song(txt):
    return clean_strings(txt)


def clean_strings(txt):
    invalid_punc = '[!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~§]'
    txt = re.sub(invalid_punc, '', txt)
    # remove 'a', 'the', and extraneous white space
    # check first if txt has more than one word, because there is an artist called "A"
    if len(txt.split()) == 1:
        return ' '.join(txt.split())
    else:
        return ' '.join([word for word in txt.split() if word.lower() not in ['the', 'a']])
