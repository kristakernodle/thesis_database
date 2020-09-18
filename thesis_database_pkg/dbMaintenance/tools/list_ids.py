from thesis_database_pkg.dbMaintenance.tools import Cursor
import thesis_database_pkg.dbMaintenance.tools.queries.select_queries as queries


def list_reviewer_ids():
    with Cursor() as cursor:
        return queries.list_all_reviewer_ids(cursor)


def list_experiment_ids():
    with Cursor() as cursor:
        return queries.list_all_experiment_ids(cursor)
