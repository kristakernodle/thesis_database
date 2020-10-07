from thesis_database import utilities as util


class BasicModel:
    def __init__(self, obj_id=None):
        self.obj_id = obj_id
        self.__model = 'basic_model'

    def __str__(self):
        return f"< {self.__class__} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, self.__class__):
            return NotImplemented
        return self.obj_id == compare_to.obj_id

    @classmethod
    def from_db_by_id(cls, primary_key=None):

        select_by_id
        a_cursor.execute("SELECT * FROM mouse WHERE mouse_id = %s;", (a_mouse_id,))
        return a_cursor.fetchone()
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
            elif self == self.from_db(eartag=self.eartag):
                return self
            else:
                update_db_entry(a_cursor)
                return self.from_db(eartag=self.eartag)

        if testing:
            with TestingCursor(postgresql) as cursor:
                if self.from_db(eartag=self.eartag) is None:
                    return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
