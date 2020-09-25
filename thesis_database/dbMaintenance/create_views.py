from thesis_database.tools import Database
from thesis_database.tools import Cursor


def create_view_all_participants_all_experiments(a_cursor):
    a_cursor.execute("""
        CREATE VIEW all_participants_all_experiments 
           (mouse_id, eartag, birthdate, genotype, experiment_id, experiment_dir, experiment_name, detail_id, 
           start_date, end_date, exp_spec_details, participant_dir) AS 
        SELECT mouse.mouse_id, mouse.eartag, mouse.birthdate, mouse.genotype, experiments.experiment_id, 
           experiments.experiment_dir, experiments.experiment_name, participant_details.detail_id, 
           participant_details.start_date, participant_details.end_date, participant_details.exp_spec_details, 
           participant_details.participant_dir
        FROM participant_details
        JOIN mouse ON mouse.mouse_id = participant_details.mouse_id
        JOIN experiments ON experiments.experiment_id = participant_details.experiment_id;
        """)


def create_view_sessions_all_upstream_ids(a_cursor):
    a_cursor.execute("""
        CREATE VIEW sessions_all_upstream 
           (mouse_id, eartag, birthdate, genotype, experiment_id, experiment_dir, experiment_name, detail_id, 
           start_date, end_date, exp_spec_details, participant_dir, session_id, session_date, session_dir, session_num) 
        AS SELECT mouse.mouse_id, mouse.eartag, mouse.birthdate, mouse.genotype, experiments.experiment_id, 
           experiments.experiment_dir, experiments.experiment_name, participant_details.detail_id, 
           participant_details.start_date, participant_details.end_date, participant_details.exp_spec_details, 
           participant_details.participant_dir, sessions.session_id, sessions.session_date, sessions.session_dir, 
           sessions.session_num
        FROM participant_details
        JOIN mouse ON mouse.mouse_id = participant_details.mouse_id
        JOIN experiments ON experiments.experiment_id = participant_details.experiment_id
        JOIN sessions ON sessions.experiment_id = experiments.experiment_id;
        """)


def create_view_folders_all_upstream_ids(a_cursor):
    a_cursor.execute("""
        CREATE VIEW folders_all_upstream 
           (mouse_id, eartag, birthdate, genotype, experiment_id, experiment_dir, experiment_name, detail_id, 
           start_date, end_date, exp_spec_details, participant_dir, session_id, session_date, session_dir, session_num,
           folder_id, folder_dir) 
        AS SELECT mouse.mouse_id, mouse.eartag, mouse.birthdate, mouse.genotype, experiments.experiment_id, 
           experiments.experiment_dir, experiments.experiment_name, participant_details.detail_id, 
           participant_details.start_date, participant_details.end_date, participant_details.exp_spec_details, 
           participant_details.participant_dir, sessions.session_id, sessions.session_date, sessions.session_dir, 
           sessions.session_num, folders.folder_id, folders.folder_dir
        FROM participant_details
        JOIN mouse ON mouse.mouse_id = participant_details.mouse_id
        JOIN experiments ON experiments.experiment_id = participant_details.experiment_id
        JOIN sessions ON sessions.experiment_id = experiments.experiment_id
        JOIN folders on folders.session_id = sessions.session_id;
        """)


def create_view_trials_all_upstream_ids(a_cursor):
    a_cursor.execute(
        "CREATE VIEW trials_all_upstream_ids "
        "   (mouse_id, experiment_id, session_id, folder_id, trial_id) AS "
        "SELECT mouse_id, trials.experiment_id, sessions.session_id, folders.folder_id, trial_id "
        "FROM trials "
        "JOIN folders on folders.folder_id = trials.folder_id "
        "JOIN sessions on sessions.experiment_id = trials.experiment_id;")


def create_view_blind_folders_all_upstream_ids(a_cursor):
    a_cursor.execute("""
        CREATE VIEW blind_folders_all_upstream_ids 
            (mouse_id, experiment_id, session_id, folder_id, reviewer_id, blind_folder_id) AS 
        SELECT sessions.mouse_id, sessions.experiment_id, 
            folders.session_id, folders.folder_id, 
            blind_folders.reviewer_id, blind_folders.blind_folder_id 
        FROM blind_folders 
        JOIN folders on folders.folder_id = blind_folders.folder_id 
        JOIN sessions on sessions.session_id = folders.session_id;
        """)


def create_view_blind_trials_all_upstream_ids(a_cursor):
    a_cursor.execute("""
    CREATE VIEW blind_trials_all_upstream_ids 
    (mouse_id, experiment_id, session_id, folder_id, trial_id, reviewer_id, blind_folder_id, blind_trial_id) AS
    SELECT sessions.mouse_id, sessions.experiment_id, sessions.session_id,
        folders.folder_id, trials.trial_id, 
        blind_folders.reviewer_id, blind_folders.blind_folder_id, 
        blind_trials.blind_trial_id
    FROM blind_trials
    JOIN trials on trials.trial_id = blind_trials.trial_id
    JOIN folders ON folders.folder_id = trials.folder_id
    JOIN sessions on sessions.session_id = folders.session_id
    JOIN blind_folders on blind_folders.folder_id = folders.folder_id;
    """)


def create_view_trial_scores_all_data(a_cursor):
    a_cursor.execute("""
        CREATE VIEW trial_scores_all_data
           (mouse_id, eartag, birthdate, genotype, experiment_id, experiment_dir, experiment_name, detail_id,
           start_date, end_date, exp_spec_details, participant_dir, session_id, session_date, session_dir, session_num,
           folder_id, folder_dir, trial_id, trial_dir, trial_date, reviewer_id, first_name, last_name, trial_score_id,
           trial_num, reach_score, abnormal_movt_score, grooming_score, blind_folder_id, blind_name, blind_trial_id,
           full_path)
        AS SELECT mouse.mouse_id, mouse.eartag, mouse.birthdate, mouse.genotype, experiments.experiment_id,
           experiments.experiment_dir, experiments.experiment_name, participant_details.detail_id,
           participant_details.start_date, participant_details.end_date, participant_details.exp_spec_details,
           participant_details.participant_dir, sessions.session_id, sessions.session_date, sessions.session_dir,
           sessions.session_num, folders.folder_id, folders.folder_dir, trials.trial_id, trials.trial_dir,
           trials.trial_date, reviewers.reviewer_id, reviewers.first_name, reviewers.last_name,
           trial_scores.trial_score_id, trial_scores.trial_num, trial_scores.reach_score,
           trial_scores.abnormal_movt_score, trial_scores.grooming_score, blind_folders.blind_folder_id,
           blind_folders.blind_name, blind_trials.blind_trial_id, blind_trials.full_path
        FROM participant_details
        JOIN mouse ON mouse.mouse_id = participant_details.mouse_id
        JOIN experiments ON experiments.experiment_id = participant_details.experiment_id
        JOIN sessions ON sessions.experiment_id = experiments.experiment_id
        JOIN folders on folders.session_id = sessions.session_id
        JOIN trials on trials.folder_id = folders.folder_id
        JOIN trial_scores on trial_scores.trial_id = trials.trial_id
        JOIN reviewers on reviewers.reviewer_id = trial_scores.reviewer_id
        JOIN blind_trials on blind_trials.trial_id = trials.trial_id
        JOIN blind_folders on blind_folders.folder_id = folders.folder_id;
    """)


def create_view_reach_score_count_by_session_id(a_cursor):
    a_cursor.execute("""
    CREATE VIEW reach_score_count_by_session_id AS
    SELECT sessions.session_id, reach_score, COUNT(reach_score) as "reach_score_count"
    FROM trial_scores
    INNER JOIN reviewers on reviewers.reviewer_id = trial_scores.reviewer_id
        INNER JOIN trials ON trial_scores.trial_id = trials.trial_id
        INNER JOIN folders on folders.folder_id = trials.folder_id
        INNER JOIN sessions on sessions.session_id = folders.session_id
    GROUP BY reach_score, sessions.session_id;
    """)


# CREATE ALL VIEWS
def create_views_main(db_details, main_user):
    Database.initialize(database=db_details['database'],
                        host=db_details['host'],
                        port=5432,
                        user=main_user['user'],
                        password=main_user['password'])
    with Cursor() as cursor:
        create_view_all_participants_all_experiments(cursor)
        create_view_folders_all_upstream_ids(cursor)
        create_view_trials_all_upstream_ids(cursor)
        create_view_blind_folders_all_upstream_ids(cursor)
        create_view_blind_trials_all_upstream_ids(cursor)
        create_view_trial_scores_all_ids(cursor)
