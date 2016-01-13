'''
Write Billboard data to a CSV file and a pickled dataframe.
'''


from bs4 import BeautifulSoup, Comment
import datetime
import codecs


def write_billboard_data(output_filename, start_date='1940-07-20', end_date='2016-01-02'):
    '''
    Populates a csv with the following fields from weekly billboard html files:
        * date:     The week the data is from
        * position: The position of the song for that week
        * title:    The song's name
        * artist:   The artist's name

    INPUTS: csv filename
    OUTPUTS: csv
    '''
    earliest_date = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    latest_date = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
    iter_week = datetime.timedelta(days=7)
    date = earliest_date

    while date <= latest_date:
        parse_html(output_filename, date)
        date = date + iter_week


def parse_html(output_filename, date):
    '''
    INPUTS: date (YYYY-MM-DD)
    OUTPUTS: None

    Adds relevant information (date, position, song, artist) from html file to data file
    '''
    filename = '../data/billboard/' + str(date) + '.html'
    with open(filename, 'r') as f:
        html_string = f.read()
    soup = BeautifulSoup(html_string, 'html.parser')
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    # Find the comment right above the table of interest
    comment = comments[comments.index(' Display Chart Table ')]
    table = comment.find_next_sibling('table')

    # Use codecs to append data on date, position, song, and artist to output file
    out_file = codecs.open(output_filename, 'a', 'utf-8')
    for i, row in enumerate(table.find_all('tr')):
        # skip header
        if i > 1:
            # create string containing date, position, song, and artist
            row_string = parse_table_row(row, date)
            out_file.write(row_string + '\n')
    out_file.close()


def parse_table_row(row, date):
    '''
    INPUTS: BeautifulSoup table row object; date
    OUTPUT: string

    Parses relevant data from table row and adds it to a list, which is converted to a string.
    '''
    row_data = row.find_all('td')
    row_to_write = []
    row_to_write.append(str(date))
    row_to_write.append(row_data[0].string.strip())
    row_to_write.append(row_data[4].find('b').string.strip())
    row_to_write.append(row_data[4].find('br').string.strip())
    return '|'.join(row_to_write)


if __name__ == '__main__':
    #TODO: Refactor to use command to delete the file, perhaps 'unlink' os.rm or os.unlink or truncate
    open('../data/billboard.csv', 'w').close()
    write_billboard_data('../data/billboard.csv')