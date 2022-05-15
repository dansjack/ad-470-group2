from flask import Flask, render_template, request, redirect, url_for
from helpers import get_db_connection

app = Flask(__name__)


@app.route("/")
def home():
    conn = get_db_connection()
    qs = conn.execute('SELECT * FROM questions').fetchall()
    print(qs)
    return render_template('qa.html', questions=qs)


@app.route('/form', methods=['GET', 'POST'])
def post_form():
    if request.method == 'POST':
        return redirect(url_for('result'), code=307)

    if request.method == 'GET':
        return render_template('form.html')

# @app.route('/add-question', methods=['POST'])
# def post_question():


@app.route('/result', methods=['POST'])
def result(question=None):
    question = request.form['question']
    return render_template('result.html', question=question)
