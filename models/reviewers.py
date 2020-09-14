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

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO reviewers (first_name, last_name, toScore_dir, scored_dir) "
                             "VALUES (%s, %s, %s, %s);",
                             (self.first_name, self.last_name, self.toScore_dir, self.scored_dir))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE reviewers "
                             "SET (first_name, last_name, toScore_dir, scored_dir) = (%s, %s, %s) "
                             "WHERE reviewer_id = %s;",
                             (self.first_name, self.last_name, self.toScore_dir, self.scored_dir, self.reviewer_id))

        def save_to_db_main(a_cursor):
            if self.from_db(scored_dir=self.scored_dir) is None:
                insert_into_db(a_cursor)
                return self.from_db(scored_dir=self.scored_dir)
            else:
                print('Reviewer already in database.')
                if self == self.from_db(scored_dir=self.scored_dir):
                    return self
                else:
                    print('This reviewer information is different from what is in the database.')
                    update = input('Do you want to update this reviewer? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(scored_dir=self.scored_dir)
                    else:
                        print('Reviewer not updated')
                        return self

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM reviewers WHERE reviewer_id = %s", (self.reviewer_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
