
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_answer(cur, content, type, parent_id=None):
    cur.execute(
        '''
        INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)
        ''',
        (parent_id, content, type))


def add_question(cur, content, type, parent_id=None):
    cur.execute(
        'INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)',
        (parent_id, content, type))


def get_comments(cur):
    return cur.execute('SELECT * FROM comments')


def get_comment(cur, comment_id):
    return cur.execute('''SELECT * FROM comments WHERE id= ?''', (comment_id,))
