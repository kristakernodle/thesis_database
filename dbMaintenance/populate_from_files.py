import os
import csv


def read_back_up_csv(fullpath):
    with open(fullpath) as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        return list(csv_reader)


def populate_mouse(back_up_mouse_full_path):
    all_mice = read_back_up_csv()


def populate_experiments():
    pass


def populate_reviewers():

    pass


def populate_participant_details():
    pass


def populate_sessions():
    pass


def populate_folders():
    pass


def populate_trials():
    pass


def populate_blind_folders():
    pass


def populate_blind_trials():
    pass


def populate_db_from_back_up_csv():
    pass



