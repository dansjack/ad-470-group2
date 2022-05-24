import json
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from helpers import get_db_connection, add_question, get_comments, add_answer, get_comment
from DocumentReader import preTrainedReader
import wikipedia as wiki

app = Flask(__name__)
print('app started')

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

model_type = 'pretrained'


@app.route("/", methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    comments = get_comments(cur).fetchall()
    conn.close()

    if request.method == 'GET':
        return render_template('qa.html', comments=comments)
    

@app.route('/change-model', methods=['POST'])
def change_model():
    print('current model type', model_type)
    data = request.get_json()
    updated_model_type = data['model_type']
    print('new type', updated_model_type)
    model_type = updated_model_type
    return 

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
    # TODO: get data from model
    conn = get_db_connection()
    cur = conn.cursor()

    data = request.get_json()
    q_id = data['question_id']
    q_text = data['question_text']
    
    print('checking wikipedia...')
    results = wiki.search(q_text)
    
    if not results:
        # no page could be found in wikipedia
        add_answer(cur, "I checked wikipedia and couldn't find a good page for your question. Please try another question.", 'bot', q_id)

        a_id = cur.lastrowid
        get_comment(cur, a_id)
        answer = cur.fetchone()

        conn.commit()
        conn.close()

        return json.dumps(tuple(answer))

    """
    START BLOCK
    This code comes from a blog, Building a QA System with BERT on Wikipedia. See https://qa.fastforwardlabs.com/pytorch/hugging%20face/wikipedia/bert/transformers/2020/05/19/Getting_Started_with_QA.html#QA-on-Wikipedia-pages
    """
    print('question:', q_text)
    try:
        page = wiki.page(results[0])
        print(f"Top wiki result: {page}")
        page_text = page.content

        preTrainedReader.tokenize(q_text, page_text)
        a_text = preTrainedReader.get_answer()
        print(f"Answer: {a_text}")
        """
        END BLOCK 
        """
        if not a_text:
            # model couldn't figure out the answer
            add_answer(cur, "You stumped me! I don't know the answer.", 'bot', q_id)

            a_id = cur.lastrowid
            get_comment(cur, a_id)
            answer = cur.fetchone()

            conn.commit()
            conn.close()

            return json.dumps(tuple(answer))
    
        # add answer to db
        add_answer(cur, a_text, 'bot', q_id)

        a_id = cur.lastrowid
        get_comment(cur, a_id)
        answer = cur.fetchone()

        conn.commit()
        conn.close()

        return json.dumps(tuple(answer))
    except Exception as e:
        print(e)
        error_string = str(e)
        
        if 'does not match any pages. Try another id!' in error_string:
            error_string = "Oops, I had a problem reading the suggested page for your question. Can you try asking something else?"

        add_answer(cur, error_string, 'bot', q_id)

        a_id = cur.lastrowid
        get_comment(cur, a_id)
        answer = cur.fetchone()

        conn.commit()
        conn.close()

        return json.dumps(tuple(answer))



