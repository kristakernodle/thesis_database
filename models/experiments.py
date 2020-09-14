from dbMaintenance.tools.cursors import TestingCursor, Cursor
import utilities as util
from dbMaintenance.tools.queries import list_all_experiments


class Experiment:
    def __init__(self, experiment_name, experiment_dir, experiment_id=None):
        self.experiment_name = util.prep_string_for_db(experiment_name)
        self.experiment_dir = experiment_dir
        self.experiment_id = experiment_id

    def __str__(self):
        return f"< Experiment {self.experiment_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Experiment):
            return NotImplemented
        return all([self.experiment_name == compare_to.experiment_name,
                    self.experiment_dir == compare_to.experiment_id,
                    self.experiment_id == compare_to.experiment_id])

    @classmethod
    def from_db(cls, experiment_name=None, experiment_id=None, testing=False, postgresql=None):
        experiment_name = util.prep_string_for_db(experiment_name)

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

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute(
                "INSERT INTO experiments(experiment_dir, experiment_name) VALUES(%s, %s);",
                (self.experiment_dir, self.experiment_name))

        def update_db_entry(a_cursor):
            a_cursor.execute(
                "UPDATE experiments SET (experiment_name, experiment_dir) = (%s, %s) WHERE experiment_id = %s;",
                (self.experiment_name, self.experiment_dir, self.experiment_id))

        def save_to_db_main(a_cursor):
            if self.experiment_name not in list_all_experiments(a_cursor):
                insert_into_db(a_cursor)
                return self.from_db(experiment_name=self.experiment_name)
            else:
                print('Experiment already in database.')
                if self == self.from_db(experiment_name=self.experiment_name):
                    return self
                else:
                    print('This experiment information is different from what is in the database.')
                    update = input('Do you want to update this experiment? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(experiment_name=self.experiment_name)
                    else:
                        print('Experiment not updated')
                        return self

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor, experiment_id):
            a_cursor.execute("DELETE FROM experiments WHERE experiment_id = %s", (experiment_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor, self.experiment_id)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor, self.experiment_id)
