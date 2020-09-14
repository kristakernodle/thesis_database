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

