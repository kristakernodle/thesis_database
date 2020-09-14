from database.cursors import Cursor, TestingCursor

import utilities as utils


def list_all_session_dir(cursor):
    cursor.execute("SELECT session_dir FROM sessions;")
    return list(item for tup in cursor.fetchall() for item in tup)


class Session:
    def __init__(self, mouse_id, experiment_id, session_dir, session_date=None, session_id=None):
        self.mouse_id = mouse_id
        self.experiment_id = experiment_id
        self.session_dir = session_dir
        self.session_date = utils.convert_date_int_yyyymmdd(session_date)
        self.session_id = session_id

    def __str__(self):
        return f"< Session {self.session_dir} >"

    def __repr__(self):
        return f"< Session {self.session_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Session):
            return NotImplemented
        return self.session_id == compare_to.session_id

    @classmethod
    def __from_db_by_id(cls, cursor, session_id):
        cursor.execute("SELECT * FROM sessions WHERE session_id = %s;", (session_id,))
        session_data = cursor.fetchone()
        if session_data is None:
            print(f"No session in the database with session_id {session_id}")
            return None
        return cls(mouse_id=session_data[1], experiment_id=session_data[2], session_date=session_data[3],
                   session_dir=session_data[4], session_id=session_data[0])

    @classmethod
    def __from_db_by_dir(cls, cursor, session_dir):
        cursor.execute("SELECT * FROM sessions WHERE session_dir = %s;", (session_dir,))
        session_data = cursor.fetchone()
        if session_data is None:
            print(f"No session in the database with directory {session_dir}")
            return None
        return cls(mouse_id=session_data[1], experiment_id=session_data[2], session_date=session_data[3],
                   session_dir=session_data[4], session_id=session_data[0])

    @classmethod
    def from_db(cls, session_id=None, session_dir=None, testing=False, postgresql=None):
        if session_dir is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_id(cursor, session_id)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_id(cursor, session_id)
        elif session_id is None:
            if testing:
                with TestingCursor(postgresql) as cursor:
                    return cls.__from_db_by_dir(cursor, session_dir)
            else:
                with Cursor() as cursor:
                    return cls.__from_db_by_dir(cursor, session_dir)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO sessions (mouse_id, experiment_id, session_date, session_dir) "
                       "VALUES (%s, %s, %s, %s);",
                       (self.mouse_id, self.experiment_id, self.session_date, self.session_dir))

    def save_to_db(self, testing=False, postgresql=None):

        def save_to_db_main(session_dir, a_cursor):
            if session_dir not in list_all_session_dir(a_cursor):
                self.__save_to_db(a_cursor)
            return self.__from_db_by_dir(a_cursor, session_dir)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(self.session_dir, cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(self.session_dir, cursor)

    # TODO: Write test for this
    @classmethod
    def list_all_sessions(cls, mouse, experiment, testing=False, postgresql=None):

        def main_list_all_sessions(a_cursor, mouse_id, experiment_id):
            a_cursor.execute("SELECT session_dir FROM sessions WHERE mouse_id = %s AND experiment_id = %s",
                             (mouse_id, experiment_id))
            return list(Session.from_db(session_dir=item) for tup in a_cursor.fetchall() for item in tup)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main_list_all_sessions(cursor, mouse.mouse_id, experiment.experiment_id)
        else:
            with Cursor() as cursor:
                return main_list_all_sessions(cursor, mouse.mouse_id, experiment.experiment_id)

    # def __delete_from_db(self, cursor):
    #     cursor.execute("DELETE FROM sessions WHERE session_id = %s", (self.session_id,))
    #
    # def delete_from_db(self, testing=False, postgresql=None):
    #     if testing:
    #         with TestingCursor(postgresql) as cursor:
    #             self.__delete_from_db(cursor)
    #     else:
    #         with Cursor() as cursor:
    #             self.__delete_from_db(cursor)
