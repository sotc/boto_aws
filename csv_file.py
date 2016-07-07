#!/usr/bin/python

import csv
import sys
from itertools import chain

'''
Generates a csv file.
'''
# work around for UnicodeEncodeError
reload(sys)
sys.setdefaultencoding("utf-8")

def write_csv(csv_filename, records, columns=None):
    '''
    Writes a CSV file to the given csv filepath using the given records dict.
    Columns are used to define the columns for the csv file.
    '''
    if columns is None:
        columns = _columns(records)

    with open(csv_filename, 'wb') as csv_fh:
        csv_writer = csv.writer(csv_fh)
        csv_writer.writerow(columns)

        for row in records:
            csv_writer.writerow([row.get(column, '') for column in columns])

def _columns(records):
    '''
    Given a list of records, determine all keys used amongst all records.
    Return this list of keys (columns).
    '''
    # sorted list of each key used among all records.
    return sorted(list(set(
      chain.from_iterable([record.keys() for record in records]))))

def csv_to_list(csv_filepath, column_names_row=0):
    '''
    Given a csv file, convert it's rows to a list of row dictionaries. Each row
    dictionary has keys of columns and values of each row's data.
    '''
    reader = csv.reader(open(csv_filepath, 'rb'))

    csv_list = []
    for row_num, row in enumerate(reader):
        if row_num == column_names_row:
            column_names = row

        if row_num > column_names_row:
            csv_list.append(dict(zip(column_names, row)))

    return csv_list
