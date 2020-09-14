import datetime
import random
import re
import string


def random_string_generator(len_string=10):
    """Generates a random string of length len_string.
    String will contain only lowercase letters and digits.
    :param len_string: length of returned string (default 10)
    :return : string of length len_string
    """

    lowercase_letters_and_digits = list(string.ascii_lowercase + string.digits)
    return ''.join(random.choices(lowercase_letters_and_digits, weights=None, k=len_string))


def convert_date_int_yyyymmdd(int_yyyymmdd):
    """Converts integer represented dates to datetime.date instances.
    :param int_yyyymmdd: integer representation of date in YYYYMMDD format.
    :return : datetime.date instance of integer date.
    """

    if isinstance(int_yyyymmdd, datetime.date):
        return int_yyyymmdd
    elif int_yyyymmdd is None:
        return None
    str_yyyymmdd = str(int_yyyymmdd)
    year = str_yyyymmdd[0:4]
    month = str_yyyymmdd[4:6]
    day = str_yyyymmdd[6:]
    date_tup = tuple(map(int, [year, month, day]))
    return datetime.date(date_tup[0], date_tup[1], date_tup[2])


def decode_genotype(genotype):
    """Converts genotype from t/f encoding to wild type/knock out encoding.
    :param genotype: 't' or 'f' value representing animal genotype
    :return : 'knock out' or 'wild type'
    """

    if type(genotype) is str:
        if genotype == 't':
            return 'knock out'
        elif genotype == 'f':
            return 'wild type'
        return genotype
    if genotype == 0:
        return 'wild type'
    return 'knock out'


def encode_genotype(genotype):
    """Converts genotype from 'knock out' or 'wild type' to True/False encoding
    :param genotype: 'knock out' or 'wild type' string
    :return : True or False encoding
    """

    if type(genotype) is bool:
        return genotype
    elif genotype == 'wild type':
        return False
    return True


def prep_string_for_db(instring):
    """Cleans string for acceptance by PostGRE database
    :param instring: string that will be inserted to the database
    :return : uniformly formatted string for database
    """

    instring_lower = instring.lower()
    split_string = re.split('[_\-/ ]', instring_lower)
    joined_string = "-".join(split_string)
    return joined_string


def list_from_cursor(cursor_fetch):
    """Generate a list of items in a cursor.
    :param cursor_fetch: a cursor with selected data
    :returns : a list of items in cursor"""

    return list(item for tup in cursor_fetch for item in tup)

#
# def read_table_csv_to_list(backup_folder_path, table_name):
#     """Converts csv file to a list containing all the information"""
#     table_filename = table_name + '.csv'
#     table_dir = os.path.join(backup_folder_path, table_filename)
#     with open(table_dir) as f:
#         contents = list(csv.reader(f))
#     return contents

