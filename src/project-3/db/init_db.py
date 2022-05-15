import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO questions (question) VALUES (?)", ('First q',))

cur.execute("INSERT INTO questions (question) VALUES (?)", ('Second qq',))

connection.commit()
connection.close()
