from flask import Flask, render_template, request, flash
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
    qs = get_questions(cur)

    if request.method == 'GET':
        return render_template('qa.html', questions=qs)

    if request.method == 'POST':
        q = request.form['question']
        if not q:
            flash('Please ask a question.')
        else:
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
            qs = get_questions(cur)
            conn.close()
        return render_template('qa.html', questions=qs)
