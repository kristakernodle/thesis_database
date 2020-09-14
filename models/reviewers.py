from dbMaintenance.tools.cursors import Cursor, TestingCursor


class Reviewer:
    def __init__(self, first_name, last_name, toScore_dir, scored_dir, reviewer_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.toScore_dir = toScore_dir
        self.scored_dir = scored_dir
        self.reviewer_id = reviewer_id

    def __str__(self):
        return f"< Reviewer {self.first_name} {self.last_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Reviewer):
            return NotImplemented
        return self.reviewer_id == compare_to.reviewer_id

    @classmethod
    def from_db(cls, reviewer_fullname=None, scored_dir=None, reviewer_id=None, testing=False, postgresql=None):

        def by_id(a_cursor, a_reviewer_id):
            a_cursor.execute("SELECT * FROM reviewers WHERE reviewer_id = %s;", (a_reviewer_id,))
            return cursor.fetchone()

        def by_scored_dir(a_cursor, a_scored_dir):
            a_cursor.execute("SELECT * FROM reviewers WHERE scored_dir = %s;", (a_scored_dir,))
            return cursor.fetchone()

        def by_fullname(a_cursor, a_reviewer_fullname):
            a_reviewer_name = a_reviewer_fullname.split(' ')
            cursor.execute("SELECT * FROM reviewers WHERE first_name = %s AND last_name = %s;",
                           (a_reviewer_name[0], a_reviewer_name[1]))
            return cursor.fetchone()

        def from_db_main(a_reviewer_fullname, a_scored_dir, a_reviewer_id, a_cursor):
            if a_reviewer_id is not None:
                reviewer_data = by_id(a_cursor, a_reviewer_id)
            elif a_scored_dir is not None:
                reviewer_data = by_scored_dir(a_cursor, a_scored_dir)
            elif a_reviewer_fullname is not None:
                reviewer_data = by_fullname(a_cursor, a_reviewer_fullname)
            else:
                reviewer_data = None

            if reviewer_data is None:
                print(f"No reviewer in the database with identifier.")
                return None
            return cls(first_name=reviewer_data[1], last_name=reviewer_data[2], toScore_dir=reviewer_data[3],
                       scored_dir=reviewer_data[4], reviewer_id=reviewer_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(reviewer_fullname, scored_dir, reviewer_id, cursor)
        else:
            with Cursor() as cursor:
                return from_db_main(reviewer_fullname, scored_dir, reviewer_id, cursor)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO reviewers (first_name, last_name, toScore_dir, scored_dir) "
                       "VALUES (%s, %s, %s, %s);", (self.first_name, self.last_name, self.toScore_dir, self.scored_dir))

    def save_to_db(self, testing=False, postgresql=None):

        def save_to_db_main(scored_dir, a_cursor):
            if scored_dir not in list_all_scored_dirs(a_cursor):
                self.__save_to_db(a_cursor)
            return self.__from_db_by_scored_dir(a_cursor, scored_dir)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(self.scored_dir, cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(self.scored_dir, cursor)

    def __delete_from_db(self, cursor):
        cursor.execute("DELETE FROM reviewers WHERE reviewer_id = %s", (self.reviewer_id,))

    def delete_from_db(self, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                self.__delete_from_db(cursor)
        else:
            with Cursor() as cursor:
                self.__delete_from_db(cursor)
