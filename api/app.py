import flask
from flask import request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

DB_PATH='data/workouts.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    return cur, conn

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

    (cur, _) = db_connection()
   
    # return the first entry from the database that matches the supplied email
    db_user = cur.execute('SELECT id, password FROM users WHERE email = :email', {"email": email}).fetchone()

    # if the returned value is None (null) this means that there is no entry with this email in the db
    if db_user is None:
        return "", 400

    # otherwise, we compare the supplied password with the hashed password from the db. if they match,
    # we return the user. otherwise, we return error.
    
    if bcrypt.checkpw(str.encode(password), str.encode(db_user['password'])):
        return jsonify({"id": db_user['id']})

    return "", 400

@app.route('/api/workouts/all', methods=['GET'])
def api_all():

    (cur, _) = db_connection()

    all_workouts = cur.execute('SELECT * FROM workouts;').fetchall()

    return jsonify(all_workouts)

@app.route('/api/user/workouts/<user_id>', methods=['GET'])
def user_workouts(user_id):
    query = "SELECT workouts.title, user_workouts.done, workouts.id FROM workouts, user_workouts  WHERE user_workouts.workout_id = workouts.id AND user_id = ?;"

    (cur, _) = db_connection()

    results = cur.execute(query, user_id).fetchall()

    return jsonify(results)

@app.route('/api/user/workouts/<user_id>/day<day_id>', methods=['GET'])
def daily_workouts(user_id, day_id):
  
    query = """
    SELECT workouts.title, exercises.name, workout_exercises.value, workout_exercises.value_type, workout_exercises.sets, user_workout_exercises.weight, exercises.video, exercises.id
    FROM user_workout_exercises, workouts, workout_exercises, exercises
    WHERE workout_exercises.exercise_id = exercises.id
    AND user_workout_exercises.workout_exercise_id = workout_exercises.id 
    AND workout_exercises.workout_id = workouts.id 
    AND workout_exercises.workout_id = ? 
    AND user_workout_exercises.user_id = ?;
    """

    (cur, _) = db_connection()

    results = cur.execute(query, [day_id,user_id]).fetchall()
    workout_details = {}
    workout_details["title"] = results[0]["title"]
    workout_details["exercises"] = []

    for exercise in results:
        workout_details["exercises"].append(
            {
                "name": exercise["name"],
                "value": exercise["value"],
                "value_type": exercise["value_type"],
                "sets": exercise["sets"],
                "weight": exercise["weight"], 
                "video": exercise["video"],
                "id": exercise["id"]
            }
        )

    return jsonify(workout_details)

@app.route('/api/user/workouts/<user_id>/day<day_id>/exercise<exercise_id>', methods=['POST'])
def weight_update(user_id, day_id, exercise_id):

    weight_info = request.json
    if not weight_info:
        return "", 400

    user_weight = weight_info['weight']

    if type(user_weight) != float:        
        try:
            user_weight = float(user_weight)         
        except ValueError:
            error_message={"message": "Please insert a number"}
            return jsonify(error_message), 400


    query = """
    select id from user_workout_exercises where user_id = ?
    and workout_exercise_id = (select id from workout_exercises 
    where workout_id = ? and exercise_id = ?);
    """

    (cur, conn) = db_connection()


    result = cur.execute(query, [user_id, day_id, exercise_id]).fetchone()
    user_workout_exercise_id = result["id"]

    query = """
    update user_workout_exercises set weight = :db_weight where id = :db_id;
    """

    cur.execute(query, {"db_weight": user_weight, "db_id": user_workout_exercise_id})
    
    conn.commit()

    return ""

@app.route('/api/user/workouts/<user_id>/<workout_id>', methods=['POST'])
def done_update(user_id, workout_id):
    done_info = request.json
    done_value = done_info['done']

    query = """
    select id from user_workouts where user_id = ?
    and workout_id = ?;
    """
    (cur, conn) = db_connection()

    user_workout_id = cur.execute(query, [user_id, workout_id]).fetchone()["id"]

    query = """
    update user_workouts 
    set done = :user_done_value where id = :workout_id_value;
    """
    cur.execute(query, {"user_done_value": done_value, "workout_id_value": user_workout_id})

    conn.commit()

    return""