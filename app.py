import collections
from flask import Flask, request, jsonify
import flask_cors
import json

from . import audio

DEBUG = True

app = Flask(__name__)

flask_cors.CORS(app, resources={r'/*': {'origins': '*'}})

def get_db():
    with open("words.db") as f:
        db = collections.Counter(json.load(f))
        
    return db

def save_db(db):
    with open("words.db", "w") as f:
        json.dump(db, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def most_frequent_words():
    if request.method == 'GET':
        db = get_db()
        
        words = [
            {"word": word,
            "frequency": frequency}
            for word, frequency in db.most_common(10)
            ]

        return jsonify({
            'status': 'success',
            'words': words
        })

    elif request.method == 'POST':
        print("trying to listen!")
        audio.listen()

        return jsonify({
            'status': 'success'
        })

@app.route('/substring', methods=['GET'])
def substring():
    sub = request.form['sub']
    db = get_db()

    matches = {
        word: db[word]
        for word in db
        if sub in word
        }

    if not matches:
        return "No words matched substring {}".format(sub)

    return matches

@app.route('/count/<word>', methods=['GET'])
def get_word_count(word):
    db = get_db()
    return "{} has been said {} times".format(word, str(db.get(word, 0)))

@app.route('/add', methods=['PUT'])
def add_word():
    db = get_db()
    word = request.form['word']

    try:
        db[word] += 1
    except KeyError:
        db[word] = 1

    save_db(db)

    return "Added {} to database".format(word)



