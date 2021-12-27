import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Georgia's and Alex's workout routine</h1>
<p>No pain no gain </p>'''


@app.route('/api/workouts/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('workouts.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_workouts = cur.execute('SELECT * FROM workouts;').fetchall()

    return jsonify(all_workouts)


@app.route('/api/user/workouts/<user_id>', methods=['GET'])
def user_workouts(user_id):
    query = "SELECT workouts.title, user_workouts.done, workouts.id FROM workouts, user_workouts  WHERE user_workouts.workout_id = workouts.id AND user_id = ?;"

    conn = sqlite3.connect('workouts.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, user_id).fetchall()

    return jsonify(results)

@app.route('/api/user/workouts/<user_id>/day<day_id>', methods=['GET'])
def daily_workouts(user_id, day_id):
    query = "SELECT exercises.name, workout_exercises.value, workout_exercises.value_type, workout_exercises.sets FROM workout_exercises, exercises, user_workouts WHERE workout_exercises.exercise_id = exercises.id AND workout_exercises.workout_id = user_workouts.workout_id AND workout_exercises.workout_id = ? AND user_id = ?;"


    conn = sqlite3.connect('workouts.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, [day_id,user_id]).fetchall()

    return jsonify(results)

app.run()