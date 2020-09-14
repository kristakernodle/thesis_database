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

