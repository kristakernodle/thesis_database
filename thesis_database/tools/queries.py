from typing import List

from thesis_database import utilities as util
from thesis_database.tools.cursors import Cursor

Column_Name_List = List[str]


def construct_basic_select(column_names: Column_Name_List, table_name: str):
    return " ".join(["SELECT", column_names, "FROM", f"{table_name};"])


def select(column_name: Column_Name_List, table_name: str):
    with Cursor() as cursor:
        cursor.execute(construct_basic_select(column_names=column_name, table_name=table_name))
        return util.list_from_cursor(cursor.fetchall())
