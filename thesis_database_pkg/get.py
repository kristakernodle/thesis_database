from thesis_database_pkg.dbMaintenance.tools import Cursor
import thesis_database_pkg.dbMaintenance.tools.queries.select_queries as queries


def list_reviewer_ids():
    with Cursor() as cursor:
        return queries.list_all_reviewer_ids(cursor)


def list_experiment_ids():
    with Cursor() as cursor:
        return queries.list_all_experiment_ids(cursor)


def list_trial_ids_for_folder(folder):
    with Cursor() as cursor:
        return queries.list_trial_ids_for_folder(cursor, folder.folder_id)


def list_all_blind_names():
    with Cursor() as cursor:
        return queries.list_all_blind_names(cursor)


def list_blind_folder_id(reviewer, folder):
    with Cursor() as cursor:
        return queries.list_blind_folder_id(cursor, reviewer.reviewer_id, folder.folder_id)
