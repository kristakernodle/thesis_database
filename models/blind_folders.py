from dbMaintenance.tools.cursors import Cursor, TestingCursor


class BlindFolder:
    def __init__(self, folder_id, reviewer_id, blind_name, blind_folder_id=None):
        self.folder_id = folder_id
        self.reviewer_id = reviewer_id
        self.blind_name = blind_name
        self.blind_folder_id = blind_folder_id

    def __str__(self):
        return f"< BlindFolder {self.blind_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, BlindFolder):
            return NotImplemented
        return all([self.folder_id == compare_to.folder_id,
                    self.reviewer_id == compare_to.reviewer_id,
                    self.blind_name == compare_to.blind_name,
                    self.blind_folder_id == compare_to.blind_folder_id])

    @classmethod
    def from_db(cls, blind_name=None, blind_folder_id=None, testing=False, postgresql=None):

        def by_blind_name(a_cursor, a_blind_name):
            a_cursor.execute("SELECT * FROM blind_folders WHERE blind_name = %s;", (a_blind_name,))
            return a_cursor.fetchone()

        def by_id(a_cursor, a_blind_folder_id):
            a_cursor.execute("SELECT * FROM blind_folders WHERE blind_folder_id = %s;", (a_blind_folder_id,))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_blind_name, a_blind_folder_id):
            if a_blind_folder_id is not None:
                blind_folder_data = by_id(a_cursor, a_blind_folder_id)
            elif a_blind_name is not None:
                blind_folder_data = by_blind_name(a_cursor, a_blind_name)
            else:
                blind_folder_data = None

            if blind_folder_data is None:
                print(f"No BlindFolder in the database with identifier.")
                return None
            return cls(folder_id=blind_folder_data[1], reviewer_id=blind_folder_data[2],
                       blind_name=blind_folder_data[3], blind_folder_id=blind_folder_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, blind_name, blind_folder_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, blind_name, blind_folder_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO blind_folders (folder_id, reviewer_id, blind_name) "
                             "VALUES (%s, %s, %s);",
                             (self.folder_id, self.reviewer_id, self.blind_name))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE blind_folders "
                             "SET (reviewer_id, blind_name) = (%s, %s) "
                             "WHERE blind_folder_id = %s;",
                             (self.reviewer_id, self.blind_name, self.folder_id))

        def save_to_db_main(a_cursor):
            if self.from_db(blind_folder_id=self.blind_folder_id) is None:
                insert_into_db(a_cursor)
                return self.from_db(blind_folder_id=self.blind_folder_id)
            else:
                print('Blind folder already in database.')
                if self == self.from_db(blind_folder_id=self.blind_folder_id):
                    return self
                else:
                    print('This blind folder information is different from what is in the database.')
                    update = input('Do you want to update this blind folder? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(blind_folder_id=self.blind_folder_id)
                    else:
                        print('Blind folder not updated')
                        return self

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM blind_folders WHERE blind_folder_id = %s", (self.blind_folder_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
