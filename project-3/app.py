import json
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from helpers import get_db_connection, add_question, get_questions, add_answer

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()


@app.route("/", methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    qs = get_questions(cur).fetchall()
    conn.close()

    if request.method == 'GET':
        return render_template('qa.html', questions=qs)


@app.route('/submit-question', methods=['POST'])
def submit_question():
    print('hi')
    data = request.get_json()
    q = data['question']
    print(q)
    conn = get_db_connection()
    cur = conn.cursor()

    # insert new question into db
    add_question(cur, q)

    # find answer from pickled model and update question record
    q_id = cur.lastrowid
    add_answer(cur, q_id, 'SOME ANSWER')

    # commit changes
    conn.commit()

    # refresh list of questions
    get_questions(cur)
    data = cur.fetchall()
    print('sending data back to template')
    conn.close()
    return json.dumps([tuple(row) for row in data])
