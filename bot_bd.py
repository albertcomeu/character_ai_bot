import psycopg2
from psycopg2 import extensions, extras


class Db:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='character_ai', user='postgres',
                                     password='1111', host='localhost')

        self.cursor = self.conn.cursor()

    def create_tabel(self):
        self.cursor.execute(
            '''CREATE TABLE USERS(
                USER_ID INTEGER,
                USERNAME TEXT,
                NAME TEXT,
                SURNAME TEXT,
                TIME TIMESTAMP,
                CHARACTER TEXT
                )''')
        self.conn.commit()

    def insert_full_data_users(self, data):
        insert_query = '''INSERT INTO USERS (USER_ID, USERNAME, NAME, SURNAME, TIME)
                        VALUES (%s,%s,%s,%s,%s)'''
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def update_character(self, user_id, character):
        update_query = '''UPDATE USERS SET CHARACTER = %s WHERE USER_ID = %s'''
        self.cursor.execute(update_query, (character, user_id))
        self.conn.commit()

    def get_rows(self):
        self.cursor.execute('''SELECT * FROM USERS''')

        users = self.cursor.fetchall()

        return users

    def drop_tabel(self):
        self.cursor.execute('''DROP TABLE Character_messages''')
        self.conn.commit()

    def create_character_tabel(self):
        self.cursor.execute(
            '''CREATE TABLE Characters(
                Hello_message TEXT,
                CHARACTER TEXT
                )''')
        self.conn.commit()

    def insert_hello_message(self, hello_message, character):
        insert_query = '''INSERT INTO Characters (Hello_message, CHARACTER)
                        VALUES (%s,%s)'''
        self.cursor.execute(insert_query, (hello_message, character))
        self.conn.commit()

    def get_hello_message(self, character):
        select_query = '''SELECT Hello_message FROM Characters WHERE CHARACTER = %s'''
        self.cursor.execute(select_query, (character,))

        message = self.cursor.fetchone()

        return message[0]

    def get_all_hello_message(self):
        self.cursor.execute('''SELECT * FROM Characters ''')
        message = self.cursor.fetchall()
        return message

    def create_message_tabel(self):
        self.cursor.execute(
            '''CREATE TABLE Character_messages(
                USER_ID TEXT,
                USER_MESSAGE TEXT,
                CHARACTER_RESPONSE TEXT,
                CHARACTER_NAME TEXT
                )''')
        self.conn.commit()

    def insert_user_message(self, user_id, user_message):
        insert_query = '''INSERT INTO Character_messages (USER_ID, USER_MESSAGE)
                        VALUES (%s,%s)'''
        self.cursor.execute(insert_query, (user_id, user_message))
        self.conn.commit()

    def insert_character_response(self, character_name, character_response, user_id):
        update_query = '''UPDATE Character_messages SET CHARACTER_NAME = %s, CHARACTER_RESPONSE = %s WHERE USER_ID = %s'''
        self.cursor.execute(update_query, (character_name, character_response, user_id))
        self.conn.commit()

    def get_messages(self):
        self.cursor.execute('''SELECT * FROM Character_messages''')

        messages = self.cursor.fetchall()

        return messages


db = Db()

# mario - Hello! It's-a me, Mario!
# Albert Enshtein - Hello I am Albert Einstein. I was born in March 14, 1879, and I conceived of the theory of special relativity and general relativity, which had a deep impact in science's understanding of physics.
