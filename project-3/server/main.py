import json
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from helpers import get_db_connection, add_question, get_comments, add_answer
from helpers import get_comment, get_wiki_answer
from DocumentReader import pretrained_reader, \
    custom_model, custom_trained_reader
from custom_model_helpers import predict
app = Flask(__name__)
print('app started')

# set up tailwind
assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

# globals for qa bot options
model_type = 'pretrained'
answer_type = 'first'


@app.route("/", methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    comments = get_comments(cur).fetchall()
    conn.close()

    if request.method == 'GET':
        return render_template(
            'qa.html',
            comments=comments,
            model_type=model_type,
            answer_type=answer_type
        )


@app.route('/change-model', methods=['POST'])
def change_model():
    global model_type
    print('current model type', model_type)
    if model_type == 'pretrained':
        model_type = 'custom'
    else:
        model_type = 'pretrained'
    print('new model type', model_type)
    return model_type


@app.route('/change-answer-type', methods=['POST'])
def change_answer_type():
    global answer_type
    print('current answer type', answer_type)
    if answer_type == 'first':
        answer_type = 'all'
        pretrained_reader.set_all_answers(True)
        custom_trained_reader.set_all_answers(True)
    else:
        answer_type = 'first'
        pretrained_reader.set_all_answers(False)
        custom_trained_reader.set_all_answers(False)
    print('new answer type', answer_type)
    return answer_type


@app.route('/submit-question', methods=['POST'])
def submit_question():
    data = request.get_json()
    q = data['question']
    conn = get_db_connection()
    cur = conn.cursor()

    # add question to db
    add_question(cur, q, 'user')

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
    q_text = data['question_text']

    print('checking wikipedia...')

    print('question:', q_text)
    reader = pretrained_reader
    print('model_type', model_type)
    if model_type == 'custom':
        reader = custom_trained_reader

    answer = get_wiki_answer(reader, q_text)
    print('answer?', answer)

    add_answer(cur, answer, 'bot', q_id)

    a_id = cur.lastrowid
    get_comment(cur, a_id)
    db_answer = cur.fetchone()

    conn.commit()
    conn.close()
    return json.dumps(tuple(db_answer))


@app.route('/generate-prediction', methods=['POST'])
def generate_short_prediction():
    data = request.get_json()
    q_text = data['question_text']
    q_context = data['question_context']

    return predict(custom_model, q_text, q_context)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0:8080", port=8080)
