from pathlib import Path


def back_up_reviewers_table(cursor, back_up_dir):
    back_up_reviewers_dir = Path(back_up_dir).joinpath('reviewers.csv')
    cursor.execute("COPY reviewers TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_reviewers_dir,))


def back_up_experiments_table(cursor, back_up_dir):
    back_up_experiments_dir = Path(back_up_dir).joinpath('experiments.csv')
    cursor.execute("COPY experiments TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_experiments_dir,))


def back_up_mouse_table(cursor, back_up_dir):
    back_up_mouse_dir = Path(back_up_dir).joinpath('mouse.csv')
    cursor.execute("COPY mouse TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_mouse_dir,))


def back_up_participant_details_table(cursor, back_up_dir):
    back_up_participant_details_dir = Path(back_up_dir).joinpath('participant_details.csv')
    cursor.execute("COPY participant_details TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_participant_details_dir,))


def back_up_sessions_table(cursor, back_up_dir):
    back_up_sessions_dir = Path(back_up_dir).joinpath('sessions.csv')
    cursor.execute("COPY sessions TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_sessions_dir,))


def back_up_folders_table(cursor, back_up_dir):
    back_up_folders_dir = Path(back_up_dir).joinpath('folders.csv')
    cursor.execute("COPY folders TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_folders_dir,))


def back_up_trials_table(cursor, back_up_dir):
    back_up_trials_dir = Path(back_up_dir).joinpath('trials.csv')
    cursor.execute("COPY trials TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_trials_dir,))


def back_up_blind_folders_table(cursor, back_up_dir):
    back_up_blind_folders_dir = Path(back_up_dir).joinpath('blind_folders.csv')
    cursor.execute("COPY trials TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_blind_folders_dir,))


def back_up_blind_trials_table(cursor, back_up_dir):
    back_up_blind_trials_dir = Path(back_up_dir).joinpath('blind_trials.csv')
    cursor.execute("COPY trials TO %s WITH DELIMITER ',' CSV HEADER;",
                   (back_up_blind_trials_dir,))
