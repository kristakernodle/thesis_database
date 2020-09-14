from dbMaintenance.tools.cursors import Cursor, TestingCursor
import utilities as util


class Mouse:
    def __init__(self, eartag, birthdate, genotype, sex, mouse_id=None):
        genotype = util.decode_genotype(genotype)

        self.eartag = int(eartag)
        self.birthdate = util.convert_date_int_yyyymmdd(birthdate)
        self.genotype = genotype
        self.sex = sex
        self.mouse_id = mouse_id

    def __str__(self):
        return f"< Mouse {self.eartag} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Mouse):
            return NotImplemented
        return self.mouse_id == compare_to.mouse_id

    @classmethod
    def from_db(cls, eartag=None, mouse_id=None, testing=False, postgresql=None):

        def by_eartag(a_cursor, a_eartag):
            a_cursor.execute("SELECT * FROM mouse WHERE eartag = %s;", (a_eartag,))
            return cursor.fetchone()

        def by_id(a_cursor, a_mouse_id):
            a_cursor.execute("SELECT * FROM mouse WHERE mouse_id = %s;", (a_mouse_id,))
            return cursor.fetchone()

        def from_db_main(a_cursor, eartag, mouse_id):
            if eartag is not None:
                mouse_data = by_eartag(a_cursor, eartag)
            elif mouse_id is not None:
                mouse_data = by_id(a_cursor, mouse_id)
            else:
                mouse_data = None

            if mouse_data is None:
                print(f"No mouse in the database with this identifier.")
                return None
            return cls(eartag=mouse_data[1], birthdate=mouse_data[2],
                       genotype=util.decode_genotype(mouse_data[3]), sex=mouse_data[4], mouse_id=mouse_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, eartag, mouse_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, eartag, mouse_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO mouse (eartag, birthdate, genotype, sex) VALUES (%s, %s, %s, %s);",
                           (self.eartag, self.birthdate, util.encode_genotype(self.genotype), self.sex))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE mouse "
                             "SET (birthdate, genotype, sex) = (%s, %s, %s) "
                             "WHERE eartag = %s;",
                             (self.birthdate, self.genotype, self.sex, self.eartag))

        def save_to_db_main(a_cursor):
            if self.from_db(eartag=self.eartag) is None:
                insert_into_db(a_cursor)
                return self.from_db(eartag=self.eartag)
            else:
                print('Mouse already in database.')
                if self == self.from_db(eartag=self.eartag):
                    return self
                else:
                    print('This mouse information is different from what is in the database.')
                    update = input('Do you want to update this mouse? [y/N]: ')
                    if update.lower() in ['y', 'yes', '1']:
                        update_db_entry(a_cursor)
                        return self.from_db(eartag=self.eartag)
                    else:
                        print('Mouse not updated')
                        return self
        if testing:
            with TestingCursor(postgresql) as cursor:
                if self.from_db(eartag=self.eartag) is None:
                    return save_to_db_main(self.eartag, cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(self.eartag, cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
