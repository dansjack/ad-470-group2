
import sqlite3
import wikipedia as wiki


def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_answer(cur, content, type, parent_id=None):
    cur.execute(
        '''
        INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)
        ''',
        (parent_id, content, type))


def add_question(cur, content, type, parent_id=None):
    cur.execute(
        'INSERT INTO comments (parent_id, content, type) VALUES (?, ?, ?)',
        (parent_id, content, type))


def get_comments(cur):
    return cur.execute('SELECT * FROM comments')


def get_comment(cur, comment_id):
    return cur.execute('''SELECT * FROM comments WHERE id= ?''', (comment_id,))


def get_wiki_answer(reader, question):
    results = wiki.search(question)

    if not results:
        # no page could be found in wikipedia
        return ("I checked wikipedia and couldn't find a good page for your ",
                "question. Please try another question.")

    try:
        """
        START BLOCK
        This code comes from a blog, Building a QA System with BERT on
        Wikipedia. See
        https://qa.fastforwardlabs.com/pytorch/hugging%20face/wikipedia/bert/transformers/2020/05/19/Getting_Started_with_QA.html#QA-on-Wikipedia-pages
        """
        page = wiki.page(results[0])
        print(f"Top wiki result: {page}")
        page_text = page.content

        reader.tokenize(question, page_text)
        a_text = reader.get_answer()
        print(f"Answer: {a_text}")
        """
        END BLOCK
        """
        if not a_text:
            # model couldn't figure out the answer
            return "You stumped me! I don't know the answer."

        return a_text
    except Exception as e:
        print(e)
        error_string = str(e)

        if 'does not match any pages. Try another id!' in error_string:
            error_string = ("Oops, I had a problem reading the suggested ",
                            "page for your question. Can you try asking ",
                            "something else?")

        # TODO: figure out what this error is
        if 'argument after ** must be a mapping, not Tensor' in error_string:
            error_string = (
                "Hmm, Wikipedia gave me some data I didn't know ",
                "how to handle. Can you try asking something else?"
                )

        return error_string
