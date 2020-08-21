from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

HIITDB = 'hiit.db'
'''
muscle_group = ['Legs','Arms', 'Core']
length = ['10mins', '15mins', '20mins']
difficulty = ['Easy', 'Medium', 'Hard']
'''
def fetchWorkout(db): #gets data from database for index.html

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


#def twentyMinutes(db):
def legs(db): #gets data from legs table for results

    legs = []
    cur = db.execute('SELECT exercise FROM legs WHERE quads == 1')
    for q in cur:
        legs.append(list(q))

    cur = db.execute('SELECT exercise FROM legs WHERE glutes == 1')
    for g in cur:
        legs.append(list(g))

    cur = db.execute('SELECT exercise FROM legs WHERE calves == 1')
    for c in cur:
        legs.append(list(c))

    jumps = []
    cur = db.execute('SELECT exercise FROM jumps WHERE legs == 1')
    for j in cur:
        legs.append(list(j))

    return {'legs':legs, 'jumps':jumps}

def armsResult(db):

    arms = []
    cur = db.execute('SELECT exercise FROM arms WHERE arms == 1')
    for a in cur:
        legs.append(list(a))

    cur = db.execute('SELECT exercise FROM arms WHERE chest == 1')
    for ch in cur:
        legs.append(list(ch))

    cur = db.execute('SELECT exercise FROM arms WHERE shoulders == 1')
    for s in cur:
        legs.append(list(s))

    jumps = []
    cur = db.execute('SELECT exercise FROM jumps WHERE arms == 1')
    for j in cur:
        legs.append(list(j))


    return {'jumps':jumps, 'arms':arms}



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

    if l == '20mins' and m == 'arms':

        db = sqlite3.connect(HIITDB)
        muscleResult = armsResult(db)
        db.close()

        return render_template('20mins.html', target=muscleResult['arms'], jumps=muscleResult['jumps']) #things that can be accessed in our .htmls

    elif l == '15mins':
         return render_template('15mins.html')
    elif l == '10mins':
        return render_template('result.html')
