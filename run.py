from flask import Flask, render_template, g, request
import sqlite3
import random

app = Flask(__name__)

hard = "50 seconds and rest for 10 seconds"
medium = "45 seconds and rest for 15 seconds"
easy = "40 seconds and rest for 20 seconds"


HIITDB = 'hiit.db'
'''
muscle_group = ['Legs','Arms', 'Core']
length = ['10mins', '15mins', '20mins']
difficulty = ['Easy', 'Medium', 'Hard']
'''

def selection(list, number):
    while len(list) > number:
        list.pop(random.randint(0,len(list)-1))


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

def coreData(db):

    core = []
    cur = db.execute('SELECT exercise FROM core')
    for co in cur:
        core.append(list(co))

    jumps = []
    cur = db.execute('SELECT exercise FROM jumps WHERE core == 1')
    for ju in cur:
        core.append(list(ju))

    return{'core':core, 'jumps':jumps}

#def twentyMinutes(db):
def legsData(db): #gets data from legs table for results

    legs = []
    cur = db.execute('SELECT exercise FROM legs')
    for q in cur:
        legs.append(list(q))

    jumps = []
    cur = db.execute('SELECT exercise, image, instructions FROM jumps WHERE legs == 1')
    for j in cur:
        legs.append(list(j))

    return {'jumps':jumps, 'legs':legs}

def armsData(db):

    arms = []
    cur = db.execute('SELECT exercise FROM arms')
    for a in cur:
        arms.append(list(a))

    jumps = []
    cur = db.execute('SELECT exercise FROM jumps WHERE arms == 1')
    for j in cur:
        arms.append(list(j))


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

    rest = ''
    print(m, l, d)
    if d == 'Hard':
        rest = '50 seconds work followed by 10 seconds rest'
    elif d == 'Medium':
        rest = '45 seconds work followed by 15 seconds rest'
    elif d == 'Easy':
        rest = '40 seconds work followed by 10 seconds rest'

#20 minutes
    if l == '20mins' and m == 'Arms':


        db = sqlite3.connect(HIITDB)
        muscleResult = armsData(db) #brings in database data
        db.close()

        selection(muscleResult['arms'], 9)

        return render_template('20mins.html', rest=rest, target=muscleResult['arms'], jumps=muscleResult['jumps']) #things that can be accessed in our .htmls

    elif l == '20mins' and m == 'Legs':

        db = sqlite3.connect(HIITDB)
        muscleResult = legsData(db)
        db.close()

        selection(muscleResult['legs'], 9)



        return render_template('20mins.html', rest=rest, target=muscleResult['legs'], jumps=muscleResult['jumps']) #things that can be accessed in our .htmls

    elif l == '20mins' and m == 'Core':

            db = sqlite3.connect(HIITDB)
            muscleResult = coreData(db)
            db.close()

            selection(muscleResult['core'], 9)


            return render_template('20mins.html', rest=rest, target=muscleResult['core'], jumps=muscleResult['jumps']) #things that can be accessed in our .htmls

#15 minutes

    elif l == '15mins' and m == 'Arms':
        db = sqlite3.connect(HIITDB)
        muscleResult = armsData(db) #brings in database data
        db.close()

        selection(muscleResult['arms'], 7)


        return render_template('15mins.html', rest=rest, target=muscleResult['arms'], jumps=muscleResult['jumps'])

    elif l == '15mins' and m == 'Legs':

        db = sqlite3.connect(HIITDB)
        muscleResult = legsData(db)
        db.close()

        selection(muscleResult['legs'], 7)

        return render_template('15mins.html', rest=rest, target=muscleResult['legs'], jumps=muscleResult['jumps'])

    elif l == '15mins' and m == 'Core':

            db = sqlite3.connect(HIITDB)
            muscleResult = coreData(db)
            db.close()

            selection(muscleResult['core'], 7)

            return render_template('15mins.html', rest=rest, target=muscleResult['core'], jumps=muscleResult['jumps'])


#10 minutes
    elif l == '10mins' and m == 'Arms':
        db = sqlite3.connect(HIITDB)
        muscleResult = armsData(db) #brings in database data
        db.close()

        selection(muscleResult['arms'], 5)

        return render_template('result.html', rest=rest, target=muscleResult['arms'], jumps=muscleResult['jumps'])

    elif l == '10mins' and m == 'Legs':

        db = sqlite3.connect(HIITDB)
        muscleResult = legsData(db)
        db.close()

        selection(muscleResult['legs'], 5)

        return render_template('result.html', rest=rest, target=muscleResult['legs'], jumps=muscleResult['jumps'])

    elif l == '10mins' and m == 'Core':

            db = sqlite3.connect(HIITDB)
            muscleResult = coreData(db)
            db.close()

            selection(muscleResult['core'], 5)

            return render_template('result.html', rest=rest, target=muscleResult['core'], jumps=muscleResult['jumps'])
