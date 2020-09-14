from dbMaintenance.tools.cursors import TestingCursor, Cursor
import utilities as utils


class Experiment:
    def __init__(self, experiment_name, experiment_dir, experiment_id=None):
        self.experiment_name = utils.prep_string_for_db(experiment_name)
        self.experiment_dir = experiment_dir
        self.experiment_id = experiment_id

    def __str__(self):
        return f"< Experiment {self.experiment_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Experiment):
            return NotImplemented
        return self.experiment_id == compare_to.experiment_id

    @classmethod
    def __from_db(cls, cursor, experiment_name):
        cursor.execute("SELECT * FROM experiments WHERE experiment_name = %s;", (experiment_name,))
        exp = cursor.fetchone()
        return cls(experiment_name=exp[2], experiment_dir=exp[1],
                   experiment_id=exp[0])

    @classmethod
    def from_db(cls, experiment_name=None, experiment_id=None, testing=False, postgresql=None):
        experiment_name = utils.prep_string_for_db(experiment_name)

        def by_experiment_name(a_cursor, exp_name):
            a_cursor.execute("SELECT * FROM experiments WHERE experiment_name = %s;", (exp_name,))
            return cursor.fetchone()

        def by_id(a_cursor, exp_id):
            a_cursor.execute("SELECT * FROM experiments WHERE experiment_id = %s;", (exp_id,))
            return cursor.fetchone()

        def from_db_main(a_cursor, exp_name, exp_id):
            if exp_name is not None:
                exp = by_experiment_name(a_cursor, exp_name)
            elif exp_id is not None:
                exp = by_id(a_cursor, exp_id)
            else:
                exp = None

            if exp is None:
                print(f"No experiment in the database with this identifier.")
                return None
            return cls(experiment_name=exp[2], experiment_dir=exp[1],
                       experiment_id=exp[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, experiment_name, experiment_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, experiment_name, experiment_id)

    @classmethod
    def get_id(cls, experiment_name, testing=False, postgresql=None):

        experiment_name = utils.prep_string_for_db(experiment_name)

        def main(a_cursor, exp_name):
            a_cursor.execute("SELECT experiment_id FROM experiments WHERE experiment_name = %s;", (exp_name,))
            exp_id = cursor.fetchall()
            if exp_id is None:
                print(f"No experiment in the database with name {exp_name}")
                return None
            return utils.list_from_cursor(exp_id)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, experiment_name)
        else:
            with Cursor() as cursor:
                return main(cursor, experiment_name)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO experiments(experiment_dir, experiment_name) VALUES(%s, %s);",
                       (self.experiment_dir, self.experiment_name))

    def __update_experiment(self, cursor):
        cursor.execute("UPDATE experiments SET (experiment_name, experiment_dir) = (%s, %s) WHERE experiment_id = %s;",
                       (self.experiment_name, self.experiment_dir, self.experiment_id))

    def save_to_db(self, testing=False, postgresql=None):

        def save_to_db_main(a_cursor):
            if self.experiment_id not in list_all_experiment_ids(a_cursor):
                self.__save_to_db(a_cursor)
            else:
                self.__update_experiment(a_cursor)
            return self.__from_db(a_cursor, self.experiment_name)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def __delete_from_db(cursor, experiment_id):
            cursor.execute("DELETE FROM experiments WHERE experiment_id = %s", (experiment_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                __delete_from_db(cursor, self.experiment_id)
        else:
            with Cursor() as cursor:
                __delete_from_db(cursor, self.experiment_id)
