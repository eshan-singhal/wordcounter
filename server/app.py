import collections
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import psycopg2

# from . import audio

DEBUG = True

app = Flask(__name__)

_DB_CONN = None

CORS(app, resources={r'/*': {'origins': '*'}})

def get_db_conn():
    global _DB_CONN
    if _DB_CONN is None:
        try:
            _DB_CONN = psycopg2.connect(
                user=os.environ.get("PGUSER"),
                password=os.environ.get("PGPASSWORD"),
                host=os.environ.get("PGHOST"),
                port=os.environ.get("PGPORT"),
                database=os.environ.get("PGDATABASE")
            )

            with _DB_CONN.cursor() as cur:

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS words
                    (
                        word varchar PRIMARY KEY NOT NULL,
                        frequency integer NOT NULL
                    );
                    """
                    )
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)

    return _DB_CONN

@app.route('/frequent', methods=['GET'])
def most_frequent_words():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM words ORDER BY frequency DESC LIMIT 10
                """
                )
        
            words = [
                {
                    "word": word,
                    "frequency": frequency
                }
                for word, frequency in cur
                ]

    return jsonify({
        'status': 'success',
        'words': words,
    })

@app.route('/listen', methods=['POST'])
def listen():
    if request.method == 'POST':
        print("trying to listen!")
        # audio.listen()

        return jsonify({
            'status': 'success'
        })

@app.route('/substring', methods=['POST'])
def substring():
    sub = request.json['sub']
    
    with get_db_conn() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT * from words WHERE word LIKE %s ESCAPE ''
                """,
                (f"%{sub}%",)
            )

            words = [
                {
                    "word": word,
                    "frequency": frequency
                }
                for word, frequency in cur
                ]

    return jsonify({
        'status': 'success',
        'words': words,
    })

@app.route('/add', methods=['PUT'])
def add_word():
    word = request.json['word']

    with get_db_conn() as conn:
        with conn.cursor() as cur:
            # This update will not do anything
            # if the word is not in the database
            cur.execute(
                """
                UPDATE words
                    SET frequency = frequency + 1
                WHERE word = (%s)
                """,
                (word,)
            )

            # This will add the word
            # if it is not in the database yet
            cur.execute(
                """
                INSERT INTO words VALUES (%s, %s)
                ON CONFLICT (word) DO NOTHING
                """,
                (word, 1)
            )

    return jsonify({
        'status': 'success'
    })

if __name__ == "main":
    app.run()