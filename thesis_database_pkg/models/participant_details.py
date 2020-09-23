from thesis_database_pkg.tools import Cursor, TestingCursor

# noinspection PyProtectedMember
from psycopg2._json import Json

from thesis_database_pkg import utilities as util
from thesis_database_pkg.models import Mouse
from thesis_database_pkg.models.experiments import Experiment


class ParticipantDetails:

    def __init__(self, mouse, experiment, participant_dir=None, start_date=None, end_date=None,
                 exp_spec_details=None, detail_id=None):
        self.mouse = mouse
        self.experiment = experiment
        self.participant_dir = participant_dir
        self.start_date = util.convert_date_int_yyyymmdd(start_date)
        self.end_date = util.convert_date_int_yyyymmdd(end_date)
        self.exp_spec_details = exp_spec_details
        self.detail_id = detail_id

    def __str__(self):
        return f"< Participant {self.mouse.eartag} in {self.experiment.experiment_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, ParticipantDetails):
            return NotImplemented
        return all([self.mouse == compare_to.mouse,
                    self.experiment == compare_to.experiment,
                    self.participant_dir == compare_to.participant_dir,
                    self.start_date == compare_to.start_date,
                    self.end_date == compare_to.end_date,
                    self.exp_spec_details == compare_to.exp_spec_details,
                    self.detail_id == compare_to.detail_id])

    @classmethod
    def from_db(cls, eartag, experiment_name, testing=False, postgresql=None):

        def from_db_main(a_cursor, a_mouse, a_experiment):
            a_cursor.execute("SELECT * FROM participant_details WHERE mouse_id = %s AND experiment_id = %s;",
                             (a_mouse.mouse_id, a_experiment.experiment_id))
            participant_details = cursor.fetchone()
            if participant_details is None:
                return None
            return cls(mouse, experiment, participant_dir=participant_details[6], start_date=participant_details[3],
                       end_date=participant_details[4],
                       exp_spec_details=participant_details[5], detail_id=participant_details[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                mouse = Mouse.from_db(eartag, testing=testing, postgresql=postgresql)
                experiment = Experiment.from_db(experiment_name, testing=testing, postgresql=postgresql)
                return from_db_main(cursor, mouse, experiment)
        else:
            with Cursor() as cursor:
                mouse = Mouse.from_db(eartag)
                experiment = Experiment.from_db(experiment_name)
                return from_db_main(cursor, mouse, experiment)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO participant_details "
                             "(mouse_id, experiment_id, start_date, end_date, exp_spec_details, participant_dir) "
                             "VALUES (%s, %s, %s, %s, %s, %s);",
                             (self.mouse.mouse_id, self.experiment.experiment_id, self.start_date, self.end_date,
                              Json(self.exp_spec_details), self.participant_dir))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE participant_details "
                             "SET (start_date, end_date, exp_spec_details, participant_dir) = (%s, %s, %s, %s) "
                             "WHERE detail_id = %s;",
                             (self.start_date, self.end_date, Json(self.exp_spec_details), self.participant_dir,
                              self.detail_id))

        def save_to_db_main(a_cursor):
            if self.from_db(self.mouse.eartag, self.experiment.experiment_name) is None:
                insert_into_db(a_cursor)
                return self.from_db(self.mouse.eartag, self.experiment.experiment_name)
            elif self == self.from_db(self.mouse.eartag, self.experiment.experiment_name):
                return self
            else:
                update_db_entry(a_cursor)
                return self.from_db(self.mouse.eartag, self.experiment.experiment_name)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM participant_details WHERE detail_id = %s", (self.detail_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
