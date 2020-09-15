
from dbMaintenance.tools.cursors import Cursor, TestingCursor


def list_all_blind_names(cursor):
    cursor.execute("SELECT blind_name FROM blind_folders;")
    return list(item for tup in cursor.fetchall() for item in tup)


class BlindFolder:
    def __init__(self, folder_id, reviewer_id, blind_name, blind_folder_id=None):
        self.folder_id = folder_id
        self.reviewer_id = reviewer_id
        self.blind_name = blind_name
        self.blind_folder_id = blind_folder_id

    def __str__(self):
        return f"< BlindFolder {self.blind_name} >"

    def __repr__(self):
        return f"< BlindFolder {self.blind_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, BlindFolder):
            return NotImplemented
        return self.blind_folder_id == compare_to.blind_folder_id

    @classmethod
    def __from_db_by_blind_name(cls, cursor, blind_name):
        cursor.execute("SELECT * FROM blind_folders WHERE blind_name = %s;", (blind_name,))
        blind_folder_data = cursor.fetchone()
        if blind_folder_data is None:
            print(f"No BlindFolder in the database with blind name {blind_name}")
            return None
        return cls(folder_id=blind_folder_data[1], reviewer_id=blind_folder_data[2], blind_name=blind_folder_data[3],
                   blind_folder_id=blind_folder_data[0])

    @classmethod
    def __from_db_by_id(cls, cursor, blind_folder_id):
        cursor.execute("SELECT * FROM blind_folders WHERE blind_folder_id = %s;", (blind_folder_id,))
        blind_folder_data = cursor.fetchone()
        if blind_folder_data is None:
            print(f"No BlindFolder in the database with blind folder ID {blind_folder_id}")
            return None
        return cls(folder_id=blind_folder_data[1], reviewer_id=blind_folder_data[2], blind_name=blind_folder_data[3],
                   blind_folder_id=blind_folder_data[0])

    @classmethod
    def from_db(cls, blind_name=None, blind_folder_id=None, testing=False, postgresql=None):
        if blind_folder_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_blind_name(cursor, blind_name)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_blind_name(cursor, blind_name)
        elif blind_name is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_id(cursor, blind_folder_id)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_id(cursor, blind_folder_id)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO blind_folders (folder_id, reviewer_id, blind_name) "
                       "VALUES (%s, %s, %s);",
                       (self.folder_id, self.reviewer_id, self.blind_name))

    def save_to_db(self, testing=False, postgresql=None):

        def save_to_db_main(blind_name, a_cursor):
            if blind_name not in list_all_blind_names(a_cursor):
                self.__save_to_db(a_cursor)
            return self.__from_db_by_blind_name(a_cursor, blind_name=blind_name)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(self.blind_name, cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(self.blind_name, cursor)

    @classmethod
    def list_all_blind_folders(cls, experiment_id, testing=False, postgresql=None):

        def main_list_all_blind_folders(a_cursor):
            a_cursor.execute("SELECT blind_folder_id FROM blind_folders_all_upstream_ids WHERE experiment_id = %s",
                             (experiment_id,))
            all_folder_ids = a_cursor.fetchall()
            return [cls.from_db(blind_folder_id=blind_folder_id[0]) for blind_folder_id in all_folder_ids]

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main_list_all_blind_folders(cursor)
        else:
            with Cursor() as cursor:
                return main_list_all_blind_folders(cursor)

    @classmethod
    def list_all_blind_names(cls, testing=False, postgresql=None):

        def main_list_all_blind_names(a_cursor):
            a_cursor.execute("SELECT blind_name FROM blind_folders;")
            return list(item for tup in a_cursor.fetchall() for item in tup)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main_list_all_blind_names(cursor)
        else:
            with Cursor() as cursor:
                return main_list_all_blind_names(cursor)
