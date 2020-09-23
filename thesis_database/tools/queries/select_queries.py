from thesis_database import utilities as util


def list_all_experiment_names(cursor):
    cursor.execute("SELECT experiment_name FROM experiments;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_mouse_eartags(cursor):
    cursor.execute("SELECT eartag FROM mouse;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_blind_names(cursor):
    cursor.execute("SELECT blind_name FROM blind_folders;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_reviewer_ids(cursor):
    cursor.execute("SELECT reviewer_id FROM reviewers;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_experiment_ids(cursor):
    cursor.execute("SELECT experiment_id FROM experiments;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_detail_ids(cursor):
    cursor.execute("SELECT detail_id FROM participant_details;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_blind_folder_ids(cursor, experiment_id):
    cursor.execute("SELECT blind_folder_id FROM blind_folders_all_upstream_ids WHERE experiment_id = %s",
                   (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())


def list_mouse_ids_for_experiment(cursor, experiment_id):
    cursor.execute("SELECT mouse_id FROM all_participants_all_trials "
                   "WHERE experiment_id = %s;", (experiment_id,))
    return sorted(set(util.list_from_cursor(cursor.fetchall())), key=int)


def list_all_folder_ids_for_experiment(cursor, experiment_id):
    cursor.execute("SELECT folder_id FROM folders_all_upstream_ids WHERE experiment_id = %s",
                   (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())


def list_all_folder_ids_for_blind_folders_of_experiment(cursor, experiment_id):
    cursor.execute("SELECT folder_id FROM blind_folders_all_upstream_ids WHERE experiment_id = %s;",
                   (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())


def list_trial_ids_for_folder(cursor, folder_id):
    cursor.execute("SELECT trial_id FROM trials WHERE folder_id = %s;", (folder_id,))
    return util.list_from_cursor(cursor.fetchall())


def list_blind_folder_id(cursor, reviewer_id, folder_id):
    cursor.execute("SELECT blind_folder_id from blind_folders WHERE reviewer_id = %s AND folder_id = %s;",
                   (reviewer_id, folder_id))
    return util.list_from_cursor(cursor.fetchall())


def list_all_reviewer_scored_dirs(cursor):
    cursor.execute("SELECT scored_dir FROM reviewers;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_session_dirs(cursor):
    cursor.execute("SELECT session_dir FROM sessions;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_folder_dirs(cursor):
    cursor.execute("SELECT folder_dir FROM folders;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_trial_dirs(cursor):
    cursor.execute("SELECT trial_dir FROM trials;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_session_dirs_for_mouse(cursor, mouse_id, experiment_id):
    cursor.execute("SELECT session_dir FROM sessions WHERE mouse_id = %s AND experiment_id = %s;",
                   (mouse_id, experiment_id))
    return util.list_from_cursor(cursor.fetchall())


def list_all_folder_dirs_for_experiment(cursor, experiment_id):
    cursor.execute("SELECT folder_dir "
                   "FROM folders "
                   "    JOIN folders_all_upstream_ids "
                   "        ON folders.folder_id = folders_all_upstream_ids.folder_id "
                   "WHERE experiment_id=%s;",
                   (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())


def list_all_trial_dirs_for_experiment(cursor, experiment_id):
    cursor.execute("SELECT trial_dir FROM trials WHERE experiment_id=%s;",
                   (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())
