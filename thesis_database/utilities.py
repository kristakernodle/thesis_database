import datetime
import re
import yaml


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


def list_of_tups_from_cursor(cursor_fetch):
    return cursor_fetch


def read_config(yaml_full_path):
    with open(yaml_full_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['dbDetails'], data['superUser'], data['mainUser'], data['reviewers']


def write_config(db_details, super_user, main_user, blind_reviewers, yaml_full_path):
    data = {'dbDetails': db_details,
            'superUser': super_user,
            'mainUser': main_user,
            'reviewers': blind_reviewers
            }
    with open(yaml_full_path, 'w+') as f:
        yaml.dump(data, f)
