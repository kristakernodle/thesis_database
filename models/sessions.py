from dbMaintenance.tools.cursors import Cursor, TestingCursor
import utilities as util


class Session:
    def __init__(self, mouse_id, experiment_id, session_dir, session_date=None, session_id=None):
        self.mouse_id = mouse_id
        self.experiment_id = experiment_id
        self.session_dir = session_dir
        self.session_date = util.convert_date_int_yyyymmdd(session_date)
        self.session_id = session_id

    def __str__(self):
        return f"< Session {self.session_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Session):
            return NotImplemented
        return all([self.mouse_id == compare_to.mouse_id,
                    self.experiment_id == compare_to.experiment_id,
                    self.session_dir == compare_to.session_dir,
                    self.session_date == compare_to.session_date,
                    self.session_id == compare_to.session_id])

    @classmethod
    def from_db(cls, session_id=None, session_dir=None, testing=False, postgresql=None):

        def by_id(a_cursor, a_session_id):
            a_cursor.execute("SELECT * FROM sessions WHERE session_id = %s;", (a_session_id,))
            return a_cursor.fetchone()

        def by_dir(a_cursor, a_session_dir):
            a_cursor.execute("SELECT * FROM sessions WHERE session_dir = %s;", (a_session_dir,))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_session_id, a_session_dir):
            if a_session_id is not None:
                session_data = by_id(a_cursor, a_session_id)
            elif a_session_dir is not None:
                session_data = by_dir(a_cursor, a_session_dir)
            else:
                session_data = None

            if session_data is None:
                print(f"No session in the database with identifier.")
                return None
            return cls(mouse_id=session_data[1], experiment_id=session_data[2], session_date=session_data[3],
                       session_dir=session_data[4], session_id=session_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, session_id, session_dir)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, session_id, session_dir)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO sessions (mouse_id, experiment_id, session_date, session_dir) "
                             "VALUES (%s, %s, %s, %s);",
                             (self.mouse_id, self.experiment_id, self.session_date, self.session_dir))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE sessions "
                             "SET (session_date, session_dir) = (%s, %s) "
                             "WHERE session_id = %s;",
                             (self.session_date, self.session_dir, self.session_id))

        def save_to_db_main(a_cursor):
            if self.from_db(session_id=self.session_id) is None:
                insert_into_db(a_cursor)
                return self.from_db(session_id=self.session_id)
            else:
                print('Session already in database.')
                if self == self.from_db(session_id=self.session_id):
                    return self
                else:
                    print('This session information is different from what is in the database.')
                    update = input('Do you want to update this session? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(session_id=self.session_id)
                    else:
                        print('Session not updated')
                        return self

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM sessions WHERE session_id = %s", (self.session_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
