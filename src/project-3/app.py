from flask import Flask, render_template, request, redirect, url_for, flash
from helpers import get_db_connection, add_question, get_questions

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    qs = get_questions(conn)

    if request.method == 'GET':
        return render_template('qa.html', questions=qs)

    if request.method == 'POST':
        q = request.form['question']
        if not q:
            flash('Please ask a question.')
        else:
            conn = get_db_connection()
            add_question(conn, q)
            qs = get_questions(conn)
            conn.close()
        return render_template('qa.html', questions=qs)
