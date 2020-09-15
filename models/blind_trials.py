from database.cursors import TestingCursor, Cursor


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
        return self.blind_trial_id == compare_to.blind_trial_id

    @classmethod
    def __from_db(cls, cursor, full_path):
        cursor.execute("SELECT * FROM blind_trials WHERE full_path = %s", (full_path,))
        blind_trial_data = cursor.fetchone()
        if blind_trial_data is None:
            print(f"No blind trial in the database with full path {full_path}")
            return None
        return cls(trial_id=blind_trial_data[1], folder_id=blind_trial_data[2],
                   full_path=blind_trial_data[3], blind_trial_id=blind_trial_data[0])

    @classmethod
    def __from_db_blind_trial_id(cls, cursor, blind_trial_id):
        cursor.execute("SELECT * FROM blind_trials WHERE blind_trial_id = %s;", (blind_trial_id,))
        blind_trial_data = cursor.fetchone()
        if blind_trial_data is None:
            print(f"No blind trial in the database with full path {blind_trial_id}")
            return None
        return cls(trial_id=blind_trial_data[1], folder_id=blind_trial_data[2],
                   full_path=blind_trial_data[3], blind_trial_id=blind_trial_data[0])

    @classmethod
    def __from_db_reviewer_trial_id(cls, cursor, reviewer_id, trial_id):
        cursor.execute("SELECT * FROM blind_trials_all_upstream_ids WHERE reviewer_id = %s and trial_id = %s;",
                       (reviewer_id, trial_id))
        blind_trial_data = cursor.fetchone()
        if blind_trial_data is None:
            print(f"No blind trial in the database with reviewer and trial id")
            return None
        return cls(trial_id=blind_trial_data[1], folder_id=blind_trial_data[2],
                   full_path=blind_trial_data[3], blind_trial_id=blind_trial_data[0])

    @classmethod
    def from_db(cls, full_path=None, blind_trial_id=None, reviewer_id=None, trial_id=None, testing=False,
                postgresql=None):
        if blind_trial_id is None and reviewer_id is None and trial_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db(cursor, full_path)
            else:
                with Cursor() as cursor:
                    return cls.__from_db(cursor, full_path)
        elif full_path is None and reviewer_id is None and trial_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_blind_trial_id(cursor, blind_trial_id)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_blind_trial_id(cursor, blind_trial_id)
        elif reviewer_id is not None and trial_id is not None and full_path is None and blind_trial_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_reviewer_trial_id(cursor, reviewer_id, trial_id)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_reviewer_trial_id(cursor, reviewer_id, trial_id)

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, full_path):
            try:
                cursor.execute(
                    "INSERT INTO blind_trials (trial_id, folder_id, full_path) VALUES (%s, %s, %s);",
                    (self.trial_id, self.folder_id, self.full_path))
            except:
                print("Already in db")
            return self.__from_db(a_cursor, full_path)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.full_path)
        else:
            with Cursor() as cursor:
                return main(cursor, self.full_path)
