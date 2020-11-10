import collections
from flask import Flask, request, jsonify
import flask_cors
import json

# from . import audio

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

@app.route('/frequent', methods=['GET'])
def most_frequent_words():
    db = get_db()
    
    words = [
        {
            "word": word,
            "frequency": frequency
        }
        for word, frequency in db.most_common(10)
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
    db = get_db()

    words = [
        {
            "word": word,
            "frequency": db[word]
        }
        for word in db
        if sub in word
        ]

    return jsonify({
        'status': 'success',
        'words': words,
    })

@app.route('/add', methods=['PUT'])
def add_word():
    db = get_db()
    word = request.json['word']

    try:
        db[word] += 1
    except KeyError:
        db[word] = 1

    save_db(db)

    return jsonify({
        'status': 'success'
    })



