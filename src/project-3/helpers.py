
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_question(conn, question):
    conn.execute('INSERT INTO questions (question) VALUES (?)', (question,))
    conn.commit()


def get_questions(conn):
    return conn.execute('SELECT * FROM questions').fetchall()
