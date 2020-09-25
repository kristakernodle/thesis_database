from thesis_database.tools import Cursor, TestingCursor


class SessionScoreCount:
    def __init__(self, session_id, reviewer_id, score0, score1, score2, score3, score4, score5, score6, score7, score8,
                 score9, abnormal_movt_score, grooming_score, session_score_count_id=None):

        self.session_id = session_id
        self.reviewer_id = reviewer_id
        self.score0 = int(score0)
        self.score1 = int(score1)
        self.score2 = int(score2)
        self.score3 = int(score3)
        self.score4 = int(score4)
        self.score5 = int(score5)
        self.score6 = int(score6)
        self.score7 = int(score7)
        self.score8 = int(score8)
        self.score9 = int(score9)
        self.abnormal_movt_score = int(abnormal_movt_score)
        self.grooming_score = int(grooming_score)
        self.session_score_count_id = session_score_count_id

    def __str__(self):
        return f"< SessionScoreCount >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, SessionScoreCount):
            return NotImplemented
        return all([self.session_id == compare_to.session_id,
                    self.reviewer_id == compare_to.reviewer_id,
                    self.score0 == compare_to.score0,
                    self.score1 == compare_to.score1,
                    self.score2 == compare_to.score2,
                    self.score3 == compare_to.score3,
                    self.score4 == compare_to.score4,
                    self.score5 == compare_to.score5,
                    self.score6 == compare_to.score6,
                    self.score7 == compare_to.score7,
                    self.score8 == compare_to.score8,
                    self.score9 == compare_to.score9,
                    self.abnormal_movt_score == compare_to.abnormal_movt_score,
                    self.grooming_score == compare_to.grooming_score,
                    self.session_score_count_id == compare_to.session_score_count_id])

    @classmethod
    def from_db(cls, session_id=None, reviewer_id=None, session_score_count_id=None, testing=False, postgresql=None):

        def by_id(a_cursor, a_session_score_count_id):
            a_cursor.execute("SELECT * FROM session_score_counts WHERE session_score_count_id = %s;",
                             (a_session_score_count_id,))
            return a_cursor.fetchone()

        def by_session_reviewer(a_cursor, a_session_id, a_reviewer_id):
            a_cursor.execute("SELECT * FROM session_score_counts WHERE session_id = %s AND reviewer_id = %s;",
                             (a_session_id, a_reviewer_id))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_session_id, a_reviewer_id, a_session_score_count_id):
            if session_score_count_id is not None:
                session_score_count_data = by_id(a_cursor, a_session_score_count_id)
            elif session_id is not None and reviewer_id is not None:
                session_score_count_data = by_session_reviewer(a_cursor, a_session_id, a_reviewer_id)
            else:
                session_score_count_data = None

            if session_score_count_data is None:
                return None
            a_session_score_count_id, a_session_id, a_reviewer_id, score0, score1, score2, score3, score4, score5, \
            score6, score7, score8, score9, abnormal_movt_score, grooming_score = session_score_count_data
            return cls(session_id=a_session_id, reviewer_id=a_reviewer_id, score0=score0, score1=score1, score2=score2,
                       score3=score3, score4=score4, score5=score5, score6=score6, score7=score7, score8=score8,
                       score9=score9, abnormal_movt_score=abnormal_movt_score, grooming_score=grooming_score)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, session_id, reviewer_id, session_score_count_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, session_id, reviewer_id, session_score_count_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO session_score_counts (session_id, reviewer_id, score0, score1, score2, "
                             "score3, score4, score5, score6, score7, score8, score9, abnormal_movt_score, "
                             "grooming_score) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                             (self.session_id, self.reviewer_id, int(self.score0), int(self.score1), int(self.score2),
                              int(self.score3), int(self.score4), int(self.score5), int(self.score6), int(self.score7),
                              int(self.score8), int(self.score9), int(self.abnormal_movt_score),
                              int(self.grooming_score)))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE session_score_counts "
                             "SET (score0, score1, score2, score3, score4, score5, score6, score7, score8, score9, "
                             "abnormal_movt_score, grooming_score) "
                             "  = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                             "WHERE session_id = %s AND reviewer_id = %s;",
                             (int(self.score0), int(self.score1), int(self.score2), int(self.score3), int(self.score4),
                              int(self.score5), int(self.score6), int(self.score7), int(self.score8), int(self.score9),
                              int(self.abnormal_movt_score), int(self.grooming_score), self.session_id,
                              self.reviewer_id))

        def save_to_db_main(a_cursor):
            if self.from_db(session_id=self.session_id, reviewer_id=self.reviewer_id) is None:
                insert_into_db(a_cursor)
                return self.from_db(session_id=self.session_id, reviewer_id=self.reviewer_id)
            elif self == self.from_db(session_id=self.session_id, reviewer_id=self.reviewer_id):
                return self
            else:
                update_db_entry(a_cursor)
                return self.from_db(session_id=self.session_id, reviewer_id=self.reviewer_id)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM session_score_counts WHERE session_score_count_id = %s",
                             (self.session_score_count_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
