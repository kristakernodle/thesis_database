from thesis_database.tools import Cursor, TestingCursor


class TrialScore:
    def __init__(self, trial_id, reviewer_id, trial_num, reach_score, abnormal_movt_score, grooming_score,
                 trial_score_id=None):

        self.trial_id = trial_id
        self.reviewer_id = reviewer_id
        self.trial_num = int(trial_num)
        self.reach_score = int(reach_score)
        self.abnormal_movt_score = int(abnormal_movt_score)
        self.grooming_score = int(grooming_score)
        self.trial_score_id = trial_score_id

    def __str__(self):
        return f"< TrialScore {self.trial_num} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, TrialScore):
            return NotImplemented
        return all([self.trial_id == compare_to.trial_id,
                    self.reviewer_id == compare_to.reviewer_id,
                    self.trial_num == compare_to.trial_num,
                    self.reach_score == compare_to.reach_score,
                    self.abnormal_movt_score == compare_to.abnormal_movt_score,
                    self.grooming_score == compare_to.grooming_score,
                    self.trial_score_id == compare_to.trial_score_id])

    @classmethod
    def from_db(cls, trial_id=None, reviewer_id=None, trial_score_id=None, testing=False, postgresql=None):

        def by_id(a_cursor, a_trial_score_id):
            a_cursor.execute("SELECT * FROM trial_scores WHERE trial_score_id = %s;", (a_trial_score_id,))
            return a_cursor.fetchone()

        def by_trial_reviewer(a_cursor, a_trial_id, a_reviewer_id):
            a_cursor.execute("SELECT * FROM trial_scores WHERE trial_id = %s AND reviewer_id = %s;",
                             (a_trial_id, a_reviewer_id))
            return a_cursor.fetchone()

        def from_db_main(a_cursor, a_trial_id, a_reviewer_id, a_trial_score_id):
            if trial_score_id is not None:
                trial_score_data = by_id(a_cursor, a_trial_score_id)
            elif trial_id is not None and reviewer_id is not None:
                trial_score_data = by_trial_reviewer(a_cursor, a_trial_id, a_reviewer_id)
            else:
                trial_score_data = None

            if trial_score_data is None:
                return None
            return cls(trial_id=trial_score_data[1], reviewer_id=trial_score_data[2],
                       trial_num=trial_score_data[3], reach_score=trial_score_data[4],
                       abnormal_movt_score=trial_score_data[5], grooming_score=trial_score_data[6],
                       trial_score_id=trial_score_data[0])

        if testing:
            with TestingCursor(postgresql) as cursor:
                return from_db_main(cursor, trial_id, reviewer_id, trial_score_id)
        else:
            with Cursor() as cursor:
                return from_db_main(cursor, trial_id, reviewer_id, trial_score_id)

    def save_to_db(self, testing=False, postgresql=None):

        def insert_into_db(a_cursor):
            a_cursor.execute("INSERT INTO trial_scores (trial_id, reviewer_id, trial_num, "
                             "  reach_score, abnormal_movt_score, grooming_score) "
                             "VALUES (%s, %s, %s, %s, %s, %s);",
                             (self.trial_id, self.reviewer_id, int(self.trial_num), int(self.reach_score),
                              bool(self.abnormal_movt_score), bool(self.grooming_score)))

        def update_db_entry(a_cursor):
            a_cursor.execute("UPDATE trial_scores "
                             "SET (trial_num, reach_score, abnormal_movt_score, grooming_score) "
                             "  = (%s, %s, %s, %s) "
                             "WHERE trial_id = %s AND reviewer_id = %s;",
                             (int(self.trial_num), int(self.reach_score), bool(self.abnormal_movt_score),
                              bool(self.grooming_score), self.trial_id, self.reviewer_id))

        def save_to_db_main(a_cursor):
            if self.from_db(trial_id=self.trial_id, reviewer_id=self.reviewer_id) is None:
                insert_into_db(a_cursor)
                return self.from_db(trial_id=self.trial_id, reviewer_id=self.reviewer_id)
            elif self == self.from_db(trial_id=self.trial_id, reviewer_id=self.reviewer_id):
                return self
            else:
                update_db_entry(a_cursor)
                return self.from_db(trial_id=self.trial_id, reviewer_id=self.reviewer_id)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    def delete_from_db(self, testing=False, postgresql=None):

        def delete_from_db_main(a_cursor):
            a_cursor.execute("DELETE FROM trial_scores WHERE trial_score_id = %s", (self.trial_score_id,))

        if testing:
            with TestingCursor(postgresql) as cursor:
                delete_from_db_main(cursor)
        else:
            with Cursor() as cursor:
                delete_from_db_main(cursor)
