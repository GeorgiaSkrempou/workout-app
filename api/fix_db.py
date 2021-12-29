import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect('data/workouts.db')
conn.row_factory = dict_factory
cur = conn.cursor()

users = cur.execute('SELECT * FROM users;').fetchall()
workouts = cur.execute('SELECT * FROM workouts;').fetchall()
exercises = cur.execute('SELECT * FROM workout_exercises;').fetchall()

for user in users:
    for workout in workouts:
        cur.execute('INSERT INTO user_workouts (user_id, workout_id, done) VALUES (:user, :workout, false)', {"user": user['id'], "workout": workout['id']})
    for exercise in exercises:
        cur.execute('INSERT INTO user_workout_exercises (user_id, workout_exercise_id, weight) VALUES (:user, :workout, false)', {"user": user['id'], "workout": exercise['id']})

conn.commit()