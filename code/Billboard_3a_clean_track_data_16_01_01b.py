# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import re



def clean_artist(txt):
    return clean_strings(txt)


def clean_song(txt):
    txt = clean_strings(txt)
    return fix_song_typos(txt)


def clean_strings(txt):
    invalid_punc = '[!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~§]'
    txt = re.sub(invalid_punc, '', txt)
    # remove 'a', 'the', and extraneous white space
    # check first if txt has more than one word, because there is an artist called "A"
    if len(txt.split()) == 1:
        return ' '.join(txt.split())
    else:
        return ' '.join([word for word in txt.split() if word.lower() not in ['the', 'a']])


def fix_song_typos(txt):
    txt = conversion_dict.get(txt, txt)
    return txt


conversion_dict = {
    'Livin On Prayer' : 'Living On Prayer',
    'Im Comin Over' : 'Im Coming Over',
    'Youre Lookin Good' : 'Youre Looking Good',
    'Im Livin In Shame' : 'Im Living In Shame',
    'You Cant Missing Nothing That You Never Had' : 'You Cant Miss Nothing That You Never Had',
    'Livin It Up' : 'Living It Up',
    'Feelin Alright' : 'Feeling Alright',
    'Hold On For Dear Love' : 'Holdin On For Dear Love',
    'Walking After Midnight' : 'Walkin After Midnight',
    'Your Bodys Callin' : 'Your Bodys Calling',
    'Twistin The Night Away' : 'Twisting The Night Away',
    'Why Im Walkin' : 'Why Im Walking',
    'These Things Will Keep Me Lovin You' : 'These Things Will Keep Me Loving You',
    'You Keep Me Hangin On' : 'You Keep Me Hanging On',
    'Sausilito' : 'Sausalito',
    'Gorver Henson Feels Forgotten' : 'Grover Henson Feels Forgotten',
    'Fraulein' : 'Freulein',
    'Pass The Curvoisier Part II' : 'Pass The Courvoisier Part II',
    'Stop Look What Your Doing' : 'Stop Look What Youre Doing',
    'Show Me What Im Loking For' : 'Show Me What Im Looking For',
    'My Favourite Girl' : 'My Favorite Girl',
    'YesSireEe' : 'YesSirEe',
    'Sweet Potatoe Pie' : 'Sweet Potato Pie',
    'Bonnie Came Back' : 'Bonnie Come Back',
    'Lonesom' : 'Lonesome',
    'Cruisng Down The River' : 'Cruising Down The River',
    'Loosing Your Love' : 'Losing Your Love',
    'Neighbor Neighbor' : 'Neighbour Neighbour',
    'Cheryl Moana Marie' : 'Cheryl Mona Marie',
    'Birthday Suite' : 'Birthday Suit',
    'Summer Souveniers' : 'Summer Souvenirs',
    'Never Leave You Uh Oooh Uh Oooh' : 'Never Leave You Uh Ooh Uh Oooh',
    'Harder To Breath' : 'Harder To Breathe',
    'More Then You Know' : 'More Than You Know',
    'Figuered You Out' : 'Figured You Out',
    'Shake Your Grove Thing' : 'Shake Your Groove Thing',
    'Ill Be Seing You' : 'Ill Be Seeing You',
    'Da Ya Think Im Sexy' : 'Do Ya Think Im Sexy',
    'Ring Dang Do' : 'Ring Dang Doo',
    'Early Morning Live' : 'Early Morning Love',
    'I Will Rememeber You' : 'I Will Remember You',
    'Summer Sweatheart' : 'Summer Sweetheart',
    'Speedoo' : 'Speedo',
    'The Angeles Listened In' : 'The Angels Listened In',
    'Souveniers' : 'Souvenirs'
    }