
def create_view_all_participants_all_experiments(a_cursor):
    a_cursor.execute(
        "CREATE VIEW all_participants_all_experiments "
        "   (mouse_id, experiment_id, detail_id, scored_dir, experiment_name, start_date, end_date) AS "
        "SELECT mouse.mouse_id, experiments.experiment_id, participant_details.detail_id, mouse.eartag, "
        "   experiments.experiment_name, participant_details.start_date, participant_details.end_date "
        "FROM participant_details "
        "JOIN mouse ON mouse.mouse_id = participant_details.mouse_id "
        "JOIN experiments ON experiments.experiment_id = participant_details.experiment_id;")


def create_view_folders_all_upstream_ids(a_cursor):
    a_cursor.execute(
        "CREATE VIEW folders_all_upstream_ids "
        "   (mouse_id, experiment_id, session_id, folder_id) AS "
        "SELECT mouse_id, sessions.experiment_id, sessions.session_id, folder_id "
        "FROM folders "
        "JOIN sessions on sessions.session_id = folders.session_id;")


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

