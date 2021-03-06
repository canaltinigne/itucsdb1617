from database import database
import psycopg2 as dbapi2


class Knot:
    def __init__(self, knot_id, owner_id, knot_content, like_counter, reknot_counter, post_date):
        self.knot_id = knot_id
        self.owner_id = owner_id
        self.knot_content = knot_content
        self.like_counter = like_counter
        self.reknot_counter = reknot_counter
        self.post_date = post_date


class KnotDatabaseOPS:
    @classmethod
    def add_knot(self, owner_id, knot_content, likes, reknots, post_date):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """INSERT INTO KNOTS (OWNER_ID, KNOT_CONTENT, LIKE_COUNTER, REKNOT_COUNTER, POST_DATE) VALUES (
                                          %s, %s, %s, %s, %s
                        )"""
            try:
                cursor.execute(query, (owner_id, knot_content, likes, reknots, post_date))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_knot(self, owner_id, knot_content, likes, reknots, post_date, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """UPDATE KNOTS SET OWNER_ID=%s, KNOT_CONTENT=%s, LIKE_COUNTER=%s,
                            REKNOT_COUNTER=%s, POST_DATE=%s  WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (owner_id, knot_content, likes, reknots, post_date, knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_knot(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """DELETE FROM KNOTS WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id,))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_knot(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """SELECT * FROM KNOTS WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id,))
                knot_data = cursor.fetchone()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if knot_data:
                return Knot(knot_data[0], knot_data[1], knot_data[2], knot_data[3],
                    knot_data[4], knot_data[5])
            else:
                return -1

    @classmethod
    def select_knots_for_owner(self, owner_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """SELECT * FROM KNOTS WHERE OWNER_ID=%s ORDER BY POST_DATE DESC"""
            knot_data = []
            knot_list = []
            try:
                cursor.execute(query, (owner_id,))
                knot_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for row in knot_data:
                knot_list.append(
                    Knot(row[0], row[1], row[2], row[3], row[4], row[5])
                )
            return knot_list


knot_ops = KnotDatabaseOPS()
