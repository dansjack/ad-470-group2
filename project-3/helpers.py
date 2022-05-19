
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_answer(cur, question_id, answer):
    cur.execute(
        '''
        UPDATE questions SET answer = ? where id = ?
        ''',
        (answer, question_id)
    )


def add_question(cur, question):
    cur.execute('INSERT INTO questions (question) VALUES (?)', (question,))


def get_questions(cur):
    return cur.execute('SELECT * FROM questions')
