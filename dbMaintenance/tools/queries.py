import utilities as util


def list_all_mouse_eartags(cursor):
    cursor.execute("SELECT eartag FROM mouse;")
    return list(item for tup in cursor.fetchall() for item in tup)


def list_all_experiments(cursor):
    cursor.execute("SELECT experiment_name FROM experiments;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_experiment_ids(cursor):
    cursor.execute("SELECT experiment_id FROM experiments;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_scored_dirs(cursor):
    cursor.execute("SELECT scored_dir FROM reviewers;")
    return list(item for tup in cursor.fetchall() for item in tup)


def list_all_reviewer_ids(cursor):
    cursor.execute("SELECT reviewer_id FROM reviewers;")
    return list(item for tup in cursor.fetchall() for item in tup)


def list_all_detail_ids(cursor):
    cursor.execute("SELECT detail_id FROM participant_details;")
    return util.list_from_cursor(cursor.fetchall())


def list_all_folder_dir(cursor):
    cursor.execute("SELECT folder_dir FROM folders;")
    return list(item for tup in cursor.fetchall() for item in tup)

def list_all_trial_dirs(cursor):
    cursor.execute("SELECT trial_dir FROM trials;")
    return list(item for tup in cursor.fetchall() for item in tup)


# @classmethod
# def list_trial_dir_for_folder(cls, folder_id, testing=False, postgresql=None):
#     if testing:
#         with TestingCursor(postgresql) as cursor:
#             cursor.execute("SELECT trial_dir FROM trials WHERE folder_id = %s;", (folder_id,))
#             return list(item for tup in cursor.fetchall() for item in tup)
#     else:
#         with Cursor() as cursor:
#             cursor.execute("SELECT trial_dir FROM trials WHERE folder_id = %s;", (folder_id,))
#             return list(item for tup in cursor.fetchall() for item in tup)
#
# @classmethod
# def list_trials_for_folder(cls, folder_id, testing=False, postgresql=None):
#     all_trial_dirs = cls.list_trial_dir_for_folder(folder_id, testing, postgresql)
#     return [cls.from_db(trial_dir=trial_dir, testing=testing, postgresql=postgresql) for trial_dir in
#             all_trial_dirs]


# @classmethod
# def list_participants(cls, experiment_name, testing=False, postgresql=None):
#
#     def main(a_cursor, experiment_id):
#         a_cursor.execute("SELECT eartag FROM all_participants_all_trials "
#                          "WHERE experiment_id = %s;", (experiment_id,))
#         no_dups = sorted(set(util.list_from_cursor(cursor.fetchall())), key=int)
#         return no_dups
#
#     experiment = Experiment.from_db(experiment_name, testing, postgresql)
#
#     if testing:
#         with TestingCursor(postgresql) as cursor:
#             return main(cursor, experiment.experiment_id)
#     else:
#         with Cursor() as cursor:
#             return main(cursor, experiment.experiment_id)


# @classmethod
# def list_all_folders(cls, experiment_id, testing=False, postgresql=None):
#
#     def main_list_all_folders(a_cursor):
#         a_cursor.execute("SELECT folder_id FROM folders_all_upstream_ids WHERE experiment_id = %s",
#                          (experiment_id,))
#         all_folder_ids = a_cursor.fetchall()
#         return [cls.from_db(folder_id=folder_id[0]) for folder_id in all_folder_ids]
#
#     if testing:
#         with TestingCursor(postgresql) as cursor:
#             return main_list_all_folders(cursor)
#     else:
#         with Cursor() as cursor:
#             return main_list_all_folders(cursor)


# # To do Write test for this
# @classmethod
# def list_all_sessions(cls, mouse, experiment, testing=False, postgresql=None):
#
#     def main_list_all_sessions(a_cursor, mouse_id, experiment_id):
#         a_cursor.execute("SELECT session_dir FROM sessions WHERE mouse_id = %s AND experiment_id = %s",
#                          (mouse_id, experiment_id))
#         return list(Session.from_db(session_dir=item) for tup in a_cursor.fetchall() for item in tup)
#
#     if testing:
#         with TestingCursor(postgresql) as cursor:
#             return main_list_all_sessions(cursor, mouse.mouse_id, experiment.experiment_id)
#     else:
#         with Cursor() as cursor:
#             return main_list_all_sessions(cursor, mouse.mouse_id, experiment.experiment_id)


# def list_participants_for_experiment(experiment_name, testing=False, postgresql=None):
#
#     def list_participants_main(a_cursor, exp_id):
#         a_cursor.execute("SELECT mouse_id FROM all_participants_all_experiments WHERE experiment_id = %s;",
#                          (exp_id,))
#         return util.list_from_cursor(cursor.fetchall())
#
#     experiment_id = Experiment.get_id(experiment_name, testing, postgresql)
#     if len(experiment_id) == 1:
#         experiment_id = experiment_id[0]
#     else:
#         warnings.warn("Multiple experiments in the database with the same name.")
#
#     if testing:
#         with TestingCursor(postgresql) as cursor:
#             return list_participants_main(cursor, experiment_id)
#     else:
#         with Cursor() as cursor:
#             return list_participants_main(cursor, experiment_id)


def list_all_session_dir(cursor):
    cursor.execute("SELECT session_dir FROM sessions;")
    return list(item for tup in cursor.fetchall() for item in tup)
