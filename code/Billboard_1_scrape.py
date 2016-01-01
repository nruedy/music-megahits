import requests
import datetime
import time



todays_date=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

def get_content_from_urls(first_date='1940-07-20', last_date=todays_date):
    '''
    INPUTS: first_date (string), last_date (string)
    OUTPUTS: None
    DESC: Writes text files with html content containing billboard data.
    The earliest date in the data is '1940-07-20'.
    '''
    index = 'http://www.umdmusic.com/default.asp?Lang=English&Chart=D'
    cur_date = datetime.datetime.strptime(last_date,'%Y-%m-%d').date()
    earliest_date = datetime.datetime.strptime(first_date,'%Y-%m-%d').date()
    iter_week = datetime.timedelta(days=7)

    while cur_date >= earliest_date:
        filename = str(cur_date) + '.html'
        f = open('../data/billboard/' + filename, 'w')
        day = cur_date.strftime('%d')
        month = cur_date.strftime('%m')
        year = cur_date.strftime('%Y')
        url_date = index + '&ChDay=' + day + '&ChMonth=' + month + '&ChYear=' + year
        f.write(requests.get(url_date).content)
        f.close()
        cur_date = cur_date - iter_week


if __name__ == '__main__':
    # to update with latest data, set first_date to the first week of missing data,
    # and last_date to the date of last available data
    get_content_from_urls(first_date='2015-12-12', last_date='2016-1-02')

