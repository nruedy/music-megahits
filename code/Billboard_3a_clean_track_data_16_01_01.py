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
    txt = txt.replace('Livin On Prayer', 'Living On Prayer')
    txt = txt.replace('Im Comin Over', 'Im Coming Over')
    txt = txt.replace('Youre Lookin Good', 'Youre Looking Good')
    txt = txt.replace('Im Livin In Shame', 'Im Living In Shame')
    txt = txt.replace('You Cant Missing Nothing That You Never Had', 'You Cant Miss Nothing That You Never Had')
    txt = txt.replace('Livin It Up', 'Living It Up')
    txt = txt.replace('Feelin Alright', 'Feeling Alright')
    txt = txt.replace('Hold On For Dear Love', 'Holdin On For Dear Love')
    txt = txt.replace('Walking After Midnight', 'Walkin After Midnight')
    txt = txt.replace('Your Bodys Callin', 'Your Bodys Calling')
    txt = txt.replace('Twistin The Night Away', 'Twisting The Night Away')
    txt = txt.replace('Why Im Walkin', 'Why Im Walking')
    txt = txt.replace('These Things Will Keep Me Lovin You', 'These Things Will Keep Me Loving You')
    txt = txt.replace('You Keep Me Hangin On', 'You Keep Me Hanging On')
    txt = txt.replace('Sausilito', 'Sausalito')
    txt = txt.replace('Gorver Henson Feels Forgotten', 'Grover Henson Feels Forgotten')
    txt = txt.replace('Fraulein', 'Freulein')
    txt = txt.replace('Pass The Curvoisier Part II', 'Pass The Courvoisier Part II')
    txt = txt.replace('Stop Look What Your Doing', 'Stop Look What Youre Doing')
    txt = txt.replace('Show Me What Im Loking For', 'Show Me What Im Looking For')
    txt = txt.replace('My Favourite Girl', 'My Favorite Girl')
    txt = txt.replace('YesSireEe', 'YesSirEe')
    txt = txt.replace('Sweet Potatoe Pie', 'Sweet Potato Pie')
    txt = txt.replace('Bonnie Came Back', 'Bonnie Come Back')
    txt = txt.replace('Lonesom', 'Lonesome')
    txt = txt.replace('Cruisng Down The River', 'Cruising Down The River')
    txt = txt.replace('Loosing Your Love', 'Losing Your Love')
    txt = txt.replace('Neighbor Neighbor', 'Neighbour Neighbour')
    txt = txt.replace('Cheryl Moana Marie', 'Cheryl Mona Marie')
    txt = txt.replace('Birthday Suite', 'Birthday Suit')
    txt = txt.replace('Summer Souveniers', 'Summer Souvenirs')
    txt = txt.replace('Never Leave You Uh Oooh Uh Oooh', 'Never Leave You Uh Ooh Uh Oooh')
    txt = txt.replace('Harder To Breath', 'Harder To Breathe')
    txt = txt.replace('More Then You Know', 'More Than You Know')
    txt = txt.replace('Figuered You Out', 'Figured You Out')
    txt = txt.replace('Shake Your Grove Thing', 'Shake Your Groove Thing')
    txt = txt.replace('Ill Be Seing You', 'Ill Be Seeing You')
    txt = txt.replace('Da Ya Think Im Sexy', 'Do Ya Think Im Sexy')
    txt = txt.replace('Ring Dang Do', 'Ring Dang Doo')
    txt = txt.replace('Early Morning Live', 'Early Morning Love')
    txt = txt.replace('I Will Rememeber You', 'I Will Remember You')
    txt = txt.replace('Summer Sweatheart', 'Summer Sweetheart')
    txt = txt.replace('Speedoo', 'Speedo')
    txt = txt.replace('The Angeles Listened In', 'The Angels Listened In')
    txt = txt.replace('Souveniers', 'Souvenirs')
    return txt
