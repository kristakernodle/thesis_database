import dbMaintenance.tools as tools


def back_up_database_to_csv_files(back_up_dir):
    with tools.Cursor() as cursor:
        tools.back_up_reviewers_table(cursor, back_up_dir)
        tools.back_up_experiments_table(cursor, back_up_dir)
        tools.back_up_mouse_table(cursor, back_up_dir)
        tools.back_up_participant_details_table(cursor, back_up_dir)
        tools.back_up_sessions_table(cursor, back_up_dir)
        tools.back_up_folders_table(cursor, back_up_dir)
        tools.back_up_trials_table(cursor, back_up_dir)
        tools.back_up_blind_folders_table(cursor, back_up_dir)
        tools.back_up_blind_trials_table(cursor, back_up_dir)
