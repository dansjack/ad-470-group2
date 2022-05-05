from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('base.html')


@app.route('/form', methods=['GET', 'POST'])
def post_form():
    if request.method == 'POST':
        return redirect(url_for('result'), code=307)

    if request.method == 'GET':
        return render_template('form.html')


@app.route('/result', methods=['POST'])
def result(question=None):
    question = request.form['question']
    return render_template('result.html', question=question)
