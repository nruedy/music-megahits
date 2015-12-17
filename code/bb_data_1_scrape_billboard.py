import requests
import datetime


def get_content_from_urls():
    '''
    INPUTS: None
    OUTPUTS: None
    DESC: Writes text files with html content containing billboard data.
        These are parsed in 'interpret_scraped_files.py'.
    '''
    index = 'http://www.umdmusic.com/default.asp?Lang=English&Chart=D'
    cur_date = datetime.datetime.strptime('2015-12-05','%Y-%m-%d').date()
    earliest_date = datetime.datetime.strptime('1940-07-20','%Y-%m-%d').date()
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
    get_content_from_urls()
