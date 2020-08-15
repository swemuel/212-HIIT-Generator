from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

HIITDB = 'hiit.db'
'''
muscle_group = ['Legs','Arms', 'Core']
length = ['10mins', '15mins', '20mins']
difficulty = ['Easy', 'Medium', 'Hard']
'''
@app.route('/')
def index():



    db = sqlite3.connect(HIITDB)

    muscle_group = []
    length = []
    difficulty = []

    cur = db.execute('SELECT muscles FROM muscle_group')
    for row in cur:
        muscle_group.append(list(row))

    cur = db.execute('SELECT length FROM length')
    for row in cur:
        length.append(list(row))

    cur = db.execute('SELECT difficulty FROM difficulty')
    for row in cur:
        difficulty.append(list(row))
    db.close()
    

    return render_template('index.html', disclaimer='no equipment required', muscles=muscle_group, length=length,
    difficulty=difficulty)


@app.route('/result', methods=['POST'])
def result():
    print(request.form)
    return render_template('result.html')
