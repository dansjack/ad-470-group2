import json
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from helpers import get_db_connection, add_question, get_comments, add_answer, get_comment

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

    # add question to db
    add_question(cur, q, 'user')

    # TODO: find answer from pickled model and add new comment
    q_id = cur.lastrowid
    get_comment(cur, q_id)
    single_data = cur.fetchone()

    conn.commit()
    conn.close()

    return json.dumps(tuple(single_data))


@app.route('/generate-answer', methods=['POST'])
def generate_answer():
    conn = get_db_connection()
    cur = conn.cursor()

    data = request.get_json()
    q_id = data['question_id']

    # add answer to db
    add_answer(cur, 'SOME ANSWER', 'bot', q_id)

    a_id = cur.lastrowid
    get_comment(cur, a_id)
    answer = cur.fetchone()

    conn.commit()
    conn.close()

    return json.dumps(tuple(answer))
