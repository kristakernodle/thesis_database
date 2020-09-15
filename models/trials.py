import utilities as util
from models.experiments import Experiment
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
        return self.trial_id == compare_to.trial_id

    @classmethod
    def __from_db_by_dir(cls, cursor, trial_dir):
        cursor.execute("SELECT * FROM trials WHERE trial_dir = %s", (trial_dir,))
        trial_data = cursor.fetchone()
        if trial_data is None:
            print(f"No trial in the database with directory {trial_dir}")
            return None
        return cls(experiment_id=trial_data[1], folder_id=trial_data[2], trial_dir=trial_data[3],
                   trial_date=trial_data[4], trial_id=trial_data[0])

    @classmethod
    def __from_db_by_id(cls, cursor, trial_id):
        cursor.execute("SELECT * FROM trials WHERE trial_id = %s", (trial_id,))
        trial_data = cursor.fetchone()
        if trial_data is None:
            print(f"No trial in the database with directory {trial_id}")
            return None
        return cls(experiment_id=trial_data[1], folder_id=trial_data[2], trial_dir=trial_data[3],
                   trial_date=trial_data[4], trial_id=trial_data[0])

    @classmethod
    def from_db(cls, trial_dir=None, trial_id=None, testing=False, postgresql=None):
        if trial_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_dir(cursor, trial_dir)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_dir(cursor, trial_dir)
        elif trial_dir is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_id(cursor, trial_id)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_id(cursor, trial_id)

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, trial_dir):
            cursor.execute(
                "INSERT INTO trials (experiment_id, folder_id, trial_dir, trial_date) VALUES (%s, %s, %s, %s);",
                (self.experiment_id, self.folder_id, self.trial_dir,
                 util.convert_date_int_yyyymmdd(self.trial_date)))
            return self.__from_db_by_dir(a_cursor, trial_dir)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.trial_dir)
        else:
            with Cursor() as cursor:
                return main(cursor, self.trial_dir)

    @classmethod
    def list_participants(cls, experiment_name, testing=False, postgresql=None):

        def main(a_cursor, experiment_id):
            a_cursor.execute("SELECT eartag FROM all_participants_all_trials "
                             "WHERE experiment_id = %s;", (experiment_id,))
            no_dups = sorted(set(util.list_from_cursor(cursor.fetchall())), key=int)
            return no_dups

        experiment = Experiment.from_db(experiment_name, testing, postgresql)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, experiment.experiment_id)
        else:
            with Cursor() as cursor:
                return main(cursor, experiment.experiment_id)

    # def __delete_from_db(self, cursor):
    #     cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))
    #
    # def delete_from_db(self, testing=False, postgresql=None):
    #     if testing:
    #         with TestingCursor(postgresql) as cursor:
    #             self.__delete_from_db(cursor)
    #     else:
    #         with Cursor() as cursor:
    #             self.__delete_from_db(cursor)

    @classmethod
    def list_trial_dir_for_folder(cls, folder_id, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                cursor.execute("SELECT trial_dir FROM trials WHERE folder_id = %s;", (folder_id,))
                return list(item for tup in cursor.fetchall() for item in tup)
        else:
            with Cursor() as cursor:
                cursor.execute("SELECT trial_dir FROM trials WHERE folder_id = %s;", (folder_id,))
                return list(item for tup in cursor.fetchall() for item in tup)

    @classmethod
    def list_trials_for_folder(cls, folder_id, testing=False, postgresql=None):
        all_trial_dirs = cls.list_trial_dir_for_folder(folder_id, testing, postgresql)
        return [cls.from_db(trial_dir=trial_dir, testing=testing, postgresql=postgresql) for trial_dir in
                all_trial_dirs]
