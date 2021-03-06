from thesis_database import utilities as util


def construct_basic_select(column_name, table_name):
    return " ".join(["SELECT", column_name, "FROM", f"{table_name};"])


def list_all_experiment_names(cursor):
    cursor.execute(construct_basic_select(column_name='experient_name', table_name='experiments'))
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
    select = construct_basic_select(column_name='experiment_id', table_name='experiments')
    cursor.execute(select)
    return util.list_from_cursor(cursor.fetchall())


def list_all_detail_ids(cursor):
    cursor.execute("SELECT detail_id FROM participant_details;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_blind_folder_ids(cursor, experiment_id):
    cursor.execute("SELECT blind_folder_id FROM blind_folders_all_upstream_ids WHERE experiment_id = %s",
                   (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())


# def list_mouse_ids_for_experiment(cursor, experiment_id):
#     cursor.execute("SELECT mouse_id FROM all_participants_all_trials "
#                    "WHERE experiment_id = %s;", (experiment_id,))
#     return sorted(set(util.list_from_cursor(cursor.fetchall())), key=int)


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
    cursor.execute("SELECT folders.folder_dir "
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


def list_all_blind_names_for_reviewer_experiment(cursor, reviewer_id, experiment_id):
    cursor.execute("SELECT blind_name "
                   "FROM blind_folders "
                   "    JOIN blind_folders_all_upstream_ids "
                   "        ON blind_folders.blind_folder_id = blind_folders_all_upstream_ids.blind_folder_id "
                   "WHERE blind_folders_all_upstream_ids.reviewer_id=%s AND experiment_id=%s;",
                   (reviewer_id, experiment_id))
    return util.list_from_cursor(cursor.fetchall())


def list_all_blind_trials_full_paths_for_reviewer_experiment(cursor, reviewer_id, experiment_id):
    cursor.execute("SELECT full_path "
                   "FROM blind_trials "
                   "    JOIN blind_trials_all_upstream_ids "
                   "        ON blind_trials.trial_id = blind_trials_all_upstream_ids.trial_id;",
                   (reviewer_id, experiment_id))
    return util.list_from_cursor(cursor.fetchall())


def list_all_session_dir_for_for_experiment(cursor, experiment_id):
    cursor.execute("SELECT session_dir "
                   "FROM sessions "
                   "WHERE experiment_id=%s;", (experiment_id,))
    return util.list_from_cursor(cursor.fetchall())


def list_engaged_reaches_by_mouse_session(cursor):
    cursor.execute("""
        SELECT eartag, session_num, engaged_reaches
            FROM
                (SELECT reach_score_count_by_session_id.session_id, SUM(reach_score_count) as "engaged_reaches"
                    FROM reach_score_count_by_session_id
                WHERE reach_score_count_by_session_id.reach_score != 0 AND reach_score_count_by_session_id.reach_score != 7
                GROUP BY reach_score_count_by_session_id.session_id) 
            AS engaged_reaching_score_count_by_session
        INNER JOIN sessions ON sessions.session_id = engaged_reaching_score_count_by_session.session_id
        INNER JOIN mouse ON mouse.mouse_id = sessions.mouse_id;
        """)
    return util.list_of_tups_from_cursor(cursor.fetchall())


def list_total_reaches_by_mouse_session(cursor):
    cursor.execute("""
        SELECT eartag, session_num, total_reaches
            FROM
                (SELECT reach_score_count_by_session_id.session_id, SUM(reach_score_count) as "total_reaches"
                    FROM reach_score_count_by_session_id
                WHERE reach_score_count_by_session_id.reach_score != 0 AND reach_score_count_by_session_id.reach_score != 7
                GROUP BY reach_score_count_by_session_id.session_id) 
            AS engaged_reaching_score_count_by_session
        INNER JOIN sessions ON sessions.session_id = engaged_reaching_score_count_by_session.session_id
        INNER JOIN mouse ON mouse.mouse_id = sessions.mouse_id;
        """)
    return util.list_of_tups_from_cursor(cursor.fetchall())
