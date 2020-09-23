from thesis_database_pkg.tools import Cursor, TestingCursor


class BlindTrial:
    def __init__(self, trial_id, folder_id, full_path, blind_trial_id=None):
        self.trial_id = trial_id
        self.folder_id = folder_id
        self.full_path = full_path
        self.blind_trial_id = blind_trial_id

    def __str__(self):
        return f"< Blind Trial {self.full_path} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, BlindTrial):
            return NotImplemented
        return all([self.trial_id == compare_to.trial_id,
                    self.folder_id == compare_to.folder_id,
                    self.full_path == compare_to.full_path,
                    self.blind_trial_id == compare_to.blind_trial_id])

    @classmethod
    def from_db(cls, full_path=None, blind_trial_id=None, reviewer_id=None, trial_id=None, testing=False,
                postgresql=None):

        def by_full_path(a_cursor, a_full_path):
            a_cursor.execute("SELECT * FROM blind_trials WHERE full_path = %s", (a_full_path,))
            return a_cursor.fetchone()

        def by_id(a_cursor, a_blind_trial_id):
            a_cursor.execute("SELECT * FROM blind_trials WHERE blind_trial_id = %s;", (a_blind_trial_id,))
            return a_cursor.fetchone()

        def by_reviewer_trial_ids(a_cursor, a_reviewer_id, a_trial_id):
            a_cursor.execute("SELECT * FROM blind_trials_all_upstream_ids WHERE reviewer_id = %s and trial_id = %s;",
                             (a_reviewer_id, a_trial_id))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_full_path, a_blind_trial_id, a_reviewer_id, a_trial_id):
            if a_blind_trial_id is not None:
                blind_trial_data = by_id(a_cursor, a_blind_trial_id)
            elif full_path is not None:
                blind_trial_data = by_full_path(a_cursor, a_full_path)
            elif reviewer_id is not None and trial_id is not None:
                blind_trial_data = by_reviewer_trial_ids(a_cursor, a_reviewer_id, a_trial_id)
            else:
                blind_trial_data = None

            if blind_trial_data is None:
                return None
            return cls(trial_id=blind_trial_data[1], folder_id=blind_trial_data[2],
                       full_path=blind_trial_data[3], blind_trial_id=blind_trial_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, full_path, blind_trial_id, reviewer_id, trial_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, full_path, blind_trial_id, reviewer_id, trial_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO blind_trials (trial_id, folder_id, full_path) VALUES (%s, %s, %s);",
                             (self.trial_id, self.folder_id, self.full_path))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE blind_trials "
                             "SET (trial_id, folder_id, full_path) = (%s, %s, %s) "
                             "WHERE blind_trial_id = %s;",
                             (self.trial_id, self.folder_id, self.full_path, self.blind_trial_id))

        def save_to_db_main(a_cursor):
            return_blind_trial_id = self.from_db(blind_trial_id=self.blind_trial_id)
            return_full_path = self.from_db(full_path=self.full_path)
            if self == return_blind_trial_id:
                return self
            elif return_blind_trial_id is None and return_full_path is None:
                insert_into_db(a_cursor)
                return self.from_db(full_path=self.full_path)
            else:
                update_db_entry(a_cursor)
                return self.from_db(full_path=self.full_path)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM blind_trials WHERE blind_trial_id = %s", (self.blind_trial_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
