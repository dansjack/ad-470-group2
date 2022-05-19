import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)",
    (None, "Welcome!", "bot",))

cur.execute(
    "INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)",
    (1, "Thanks!", "user",))

connection.commit()
connection.close()
