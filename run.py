from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

HIITDB = 'hiit.db'
'''
muscle_group = ['Legs','Arms', 'Core']
length = ['10mins', '15mins', '20mins']
difficulty = ['Easy', 'Medium', 'Hard']
'''
def fetchWorkout(db):

    muscle_group = []
    cur = db.execute('SELECT muscles FROM muscle_group')
    for row in cur:
        muscle_group.append(list(row))

    length = []
    cur = db.execute('SELECT length FROM length')
    for row in cur:
        length.append(list(row))

    difficulty = []
    cur = db.execute('SELECT difficulty FROM difficulty')
    for row in cur:
        difficulty.append(list(row))


    return {'muscle_group':muscle_group, 'length':length, 'difficulty':difficulty}


def twentyMinutes(db):

    legs = []
    cur = db.execute('SELECT exercise FROM legs WHERE quads == 1')
    for q in cur:
        legs.append(list(q))

    cur = db.execute('SELECT exercise FROM legs WHERE glutes == 1')
    for g in cur:
        legs.append(list(g))

    print(r)

    return {'legs':legs}





@app.route('/')
def index():


    db = sqlite3.connect(HIITDB)
    workout = fetchWorkout(db)
    db.close()

    return render_template('index.html',
    disclaimer='no equipment required',
    muscles=workout['muscle_group'],
    length=workout['length'],
    difficulty=workout['difficulty']
    )


@app.route('/result', methods=['POST'])
def result():
    db = sqlite3.connect(HIITDB)
    workout = fetchWorkout(db)
    db.close()
    m = (request.form['muscle'])
    l = (request.form['length'])
    d = (request.form['difficulty'])
    print(m, l, d)

    if l == '20mins':

        db = sqlite3.connect(HIITDB)
        workout = twentyMinutes(db)
        db.close()

        return render_template('20mins.html', legs=workout['legs'])

    elif l == '15mins':
         return render_template('15mins.html')
    elif l == '10mins':
        return render_template('result.html')
