from thesis_database_pkg.tools import Database
import psycopg2


class Cursor:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Executed when we enter the 'with' statement
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_val, exception_traceback):
        # Executed when we exit the 'with' statement
        if exception_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.put_connection(self.connection)


class TestingCursor:
    def __init__(self, postgresql):
        self.connection = None
        self.cursor = None
        self.postgresql = postgresql

    def __enter__(self):
        self.connection = psycopg2.connect(**self.postgresql.dsn())
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_val, exception_traceback):
        if exception_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        self.connection.close()
