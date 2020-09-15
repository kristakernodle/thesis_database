import utilities as util
from dbMaintenance.tools.cursors import Cursor, TestingCursor


class Trial:

    def __init__(self, experiment_id, folder_id, trial_dir, trial_date, trial_id=None):
        self.experiment_id = experiment_id
        self.folder_id = folder_id
        self.trial_dir = trial_dir
        self.trial_date = util.convert_date_int_yyyymmdd(trial_date)
        self.trial_id = trial_id

    def __str__(self):
        return f"< Trial {self.trial_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Trial):
            return NotImplemented
        return all([self.experiment_id == compare_to.experiment_id,
                    self.folder_id == compare_to.folder_id,
                    self.trial_dir == compare_to.trial_dir,
                    self.trial_date == compare_to.trial_date,
                    self.trial_id == compare_to.trial_id])

    @classmethod
    def from_db(cls, trial_dir=None, trial_id=None, testing=False, postgresql=None):
        def by_dir(a_cursor, a_trial_dir):
            a_cursor.execute("SELECT * FROM trials WHERE trial_dir = %s", (a_trial_dir,))
            return a_cursor.fetchone()

        def by_id(a_cursor, a_trial_id):
            a_cursor.execute("SELECT * FROM trials WHERE trial_id = %s", (a_trial_id,))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_trial_dir, a_trial_id):
            if a_trial_id is not None:
                trial_data = by_id(a_cursor, a_trial_id)
            elif a_trial_dir is not None:
                trial_data = by_dir(a_cursor, a_trial_dir)
            else:
                trial_data = None

            if trial_data is None:
                print(f"No trial in the database with directory {a_trial_id}")
                return None
            return cls(experiment_id=trial_data[1], folder_id=trial_data[2], trial_dir=trial_data[3],
                       trial_date=trial_data[4], trial_id=trial_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, trial_dir, trial_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, trial_dir, trial_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute(
                "INSERT INTO trials (experiment_id, folder_id, trial_dir, trial_date) VALUES (%s, %s, %s, %s);",
                (self.experiment_id, self.folder_id, self.trial_dir,
                 util.convert_date_int_yyyymmdd(self.trial_date)))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE trials "
                             "SET (trial_dir, trial_date) = (%s, %s) "
                             "WHERE trial_id = %s;",
                             (self.trial_dir, self.trial_date, self.trial_id))

        def save_to_db_main(a_cursor):
            if self.from_db(trial_id=self.trial_id) is None:
                insert_into_db(a_cursor)
                return self.from_db(trial_id=self.trial_id)
            else:
                print('Trial already in database.')
                if self == self.from_db(trial_id=self.trial_id):
                    return self
                else:
                    print('This trial information is different from what is in the database.')
                    update = input('Do you want to update this trial? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(trial_id=self.trial_id)
                    else:
                        print('Trial not updated')
                        return self

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM trials WHERE trial_id = %s", (self.trial_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
