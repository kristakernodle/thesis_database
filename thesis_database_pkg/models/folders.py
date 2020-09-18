from thesis_database_pkg.dbMaintenance.tools import Cursor, TestingCursor


class Folder:
    def __init__(self, session_id, folder_dir, folder_id=None):
        self.session_id = session_id
        self.folder_dir = folder_dir
        self.folder_id = folder_id

    def __str__(self):
        return f"< Folder {self.folder_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Folder):
            return NotImplemented
        return all([self.folder_dir == compare_to.folder_dir,
                    self.session_id == compare_to.session_id,
                    self.folder_id == compare_to.folder_id])

    @classmethod
    def from_db(cls, folder_dir=None, folder_id=None, testing=False, postgresql=None):

        def by_id(a_cursor, a_folder_id):
            a_cursor.execute("SELECT * FROM folders WHERE folder_id = %s;", (a_folder_id,))
            return a_cursor.fetchone()

        def by_dir(a_cursor, a_folder_dir):
            a_cursor.execute("SELECT * FROM folders WHERE folder_dir = %s;", (a_folder_dir,))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_folder_dir, a_folder_id):
            if a_folder_id is not None:
                folder_data = by_id(a_cursor, a_folder_id)
            elif a_folder_dir is not None:
                folder_data = by_dir(a_cursor, a_folder_dir)
            else:
                folder_data = None

            if folder_data is None:
                print(f"No folder in the database with identifier.")
                return None
            return cls(session_id=folder_data[1], folder_dir=folder_data[2], folder_id=folder_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, folder_dir, folder_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, folder_dir, folder_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO folders (session_id, folder_dir) "
                             "VALUES (%s, %s);",
                             (self.session_id, self.folder_dir))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE folders "
                             "SET (session_id, folder_dir) = (%s, %s) "
                             "WHERE folder_id = %s;",
                             (self.session_id, self.folder_dir, self.folder_id))

        def save_to_db_main(a_cursor):
            if self.from_db(folder_id=self.folder_id) is None:
                insert_into_db(a_cursor)
                return self.from_db(folder_id=self.folder_id)
            else:
                print('Folder already in database.')
                if self == self.from_db(folder_id=self.folder_id):
                    return self
                else:
                    print('This folder information is different from what is in the database.')
                    update = input('Do you want to update this folder? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(folder_id=self.folder_id)
                    else:
                        print('Folder not updated')
                        return self
        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM folders WHERE folder_id = %s", (self.folder_id,))
        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)


