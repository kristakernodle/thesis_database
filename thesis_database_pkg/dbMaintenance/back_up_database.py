import thesis_database_pkg.tools as tools
import shutil
from pathlib import Path


def back_up_database_to_csv_files(back_up_dir):
    temp_dir = '/tmp/'
    with tools.Cursor() as cursor:
        tools.back_up_reviewers_table(cursor, temp_dir)
        tools.back_up_experiments_table(cursor, temp_dir)
        tools.back_up_mouse_table(cursor, temp_dir)
        tools.back_up_participant_details_table(cursor, temp_dir)
        tools.back_up_sessions_table(cursor, temp_dir)
        tools.back_up_folders_table(cursor, temp_dir)
        tools.back_up_trials_table(cursor, temp_dir)
        tools.back_up_blind_folders_table(cursor, temp_dir)
        tools.back_up_blind_trials_table(cursor, temp_dir)
    for back_up_csv in Path(temp_dir).glob('*_back_up.csv'):
        shutil.copy(back_up_csv, back_up_dir)


def back_up_database(db_details, main_user):
    tools.Database.initialize(database=db_details['database'],
                              host=db_details['host'],
                              port=5432,
                              user=main_user['user'],
                              password=main_user['password'])
    back_up_database_to_csv_files(db_details['backupDir'])
