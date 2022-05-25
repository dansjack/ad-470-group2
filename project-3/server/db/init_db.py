import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)",
    (None, "Welcome! What would you like to know?", "bot",))

connection.commit()
connection.close()
