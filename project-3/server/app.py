import json
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from helpers import get_db_connection, add_question, get_comments, get_comment, add_answer

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()


@app.route("/", methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    comments = get_comments(cur).fetchall()
    conn.close()

    if request.method == 'GET':
        return render_template('qa.html', comments=comments)


@app.route('/submit-question', methods=['POST'])
def submit_question():
    data = request.get_json()
    q = data['question']
    conn = get_db_connection()
    cur = conn.cursor()

    # insert new question into db
    add_question(cur, q, 'user')

    # TODO: find answer from pickled model and update question record
    q_id = cur.lastrowid
    print('q_id', q_id)
    # q = get_comment(cur, q_id)
    # print(json.dumps([tuple(row) for row in q]))
    add_answer(cur, 'SOME ANSWER', 'bot', q_id)

    # commit changes
    conn.commit()

    # refresh list of questions
    get_comments(cur)
    data = cur.fetchall()
    print('sending data back to template')
    conn.close()
    return json.dumps([tuple(row) for row in data])
