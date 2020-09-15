from database.cursors import Cursor, TestingCursor


def list_all_folder_dir(cursor):
    cursor.execute("SELECT folder_dir FROM folders;")
    return list(item for tup in cursor.fetchall() for item in tup)


class Folder:
    def __init__(self, session_id, folder_dir, folder_id=None):
        self.session_id = session_id
        self.folder_dir = folder_dir
        self.folder_id = folder_id

    def __str__(self):
        return f"< Folder {self.folder_dir} >"

    def __repr__(self):
        return f"< Folder {self.folder_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Folder):
            return NotImplemented
        return self.folder_id == compare_to.folder_id

    @classmethod
    def __from_db_by_dir(cls, cursor, folder_dir):
        cursor.execute("SELECT * FROM folders WHERE folder_dir = %s;", (folder_dir,))
        folder_data = cursor.fetchone()
        if folder_data is None:
            print(f"No folder in the database with directory {folder_dir}")
            return None
        return cls(session_id=folder_data[1], folder_dir=folder_data[2], folder_id=folder_data[0])

    @classmethod
    def __from_db_by_id(cls, cursor, folder_id):
        cursor.execute("SELECT * FROM folders WHERE folder_id = %s;", (folder_id,))
        folder_data = cursor.fetchone()
        if folder_data is None:
            print(f"No folder in the database with ID {folder_id}")
            return None
        return cls(session_id=folder_data[1], folder_dir=folder_data[2], folder_id=folder_data[0])

    @classmethod
    def from_db(cls, folder_dir=None, folder_id=None, testing=False, postgresql=None):
        if folder_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_dir(cursor, folder_dir)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_dir(cursor, folder_dir)
        elif folder_dir is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_id(cursor, folder_id)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_id(cursor, folder_id)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO folders (session_id, folder_dir) "
                       "VALUES (%s, %s);",
                       (self.session_id, self.folder_dir))

    def save_to_db(self, testing=False, postgresql=None):

        def save_to_db_main(folder_dir, a_cursor):
            if folder_dir not in list_all_folder_dir(a_cursor):
                self.__save_to_db(a_cursor)
            return self.__from_db_by_dir(a_cursor, folder_dir)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(self.folder_dir, cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(self.folder_dir, cursor)

    # def __delete_from_db(self, cursor):
    #     cursor.execute("DELETE FROM folders WHERE folder_id = %s", (self.folder_id,))
    #
    # def delete_from_db(self, testing=False, postgresql=None):
    #     if testing:
    #         with TestingCursor(postgresql) as cursor:
    #             self.__delete_from_db(cursor)
    #     else:
    #         with Cursor() as cursor:
    #             self.__delete_from_db(cursor)

    @classmethod
    def list_all_folders(cls, experiment_id, testing=False, postgresql=None):

        def main_list_all_folders(a_cursor):
            a_cursor.execute("SELECT folder_id FROM folders_all_upstream_ids WHERE experiment_id = %s",
                             (experiment_id,))
            all_folder_ids = a_cursor.fetchall()
            return [cls.from_db(folder_id=folder_id[0]) for folder_id in all_folder_ids]

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main_list_all_folders(cursor)
        else:
            with Cursor() as cursor:
                return main_list_all_folders(cursor)

