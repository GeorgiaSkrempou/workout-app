import flask
from flask import request, jsonify
import sqlite3
import bcrypt

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DB_PATH='api/data/workouts.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Georgia's and Alex's workout routine</h1>
<p>No pain no gain </p>'''

@app.route('/api/login', methods=['POST'])
def login():
    user_info = request.json
    if not user_info:
        return "", 400

    email = user_info['email']
    password = user_info['password']

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    # return the first entry from the database that matches the supplied email
    db_user = cur.execute('SELECT id, password FROM users WHERE email = :email', {"email": email}).fetchone()

    # if the returned value is None (null) this means that there is no entry with this email in the db
    if db_user is None:
        return "", 400

    # otherwise, we compare the supplied password with the hashed password from the db. if they match,
    # we return the user. otherwise, we return error.
    
    if bcrypt.checkpw(str.encode(password), str.encode(db_user['password'])):
        return {"id": db_user['id']}

    return "", 400


@app.route('/api/workouts/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_workouts = cur.execute('SELECT * FROM workouts;').fetchall()

    return jsonify(all_workouts)


@app.route('/api/user/workouts/<user_id>', methods=['GET'])
def user_workouts(user_id):
    query = "SELECT workouts.title, user_workouts.done, workouts.id FROM workouts, user_workouts  WHERE user_workouts.workout_id = workouts.id AND user_id = ?;"

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, user_id).fetchall()

    return jsonify(results)

@app.route('/api/user/workouts/<user_id>/day<day_id>', methods=['GET'])
def daily_workouts(user_id, day_id):
    query = "SELECT exercises.name, workout_exercises.value, workout_exercises.value_type, workout_exercises.sets FROM workout_exercises, exercises, user_workouts WHERE workout_exercises.exercise_id = exercises.id AND workout_exercises.workout_id = user_workouts.workout_id AND workout_exercises.workout_id = ? AND user_id = ?;"


    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, [day_id,user_id]).fetchall()

    return jsonify(results)

app.run()