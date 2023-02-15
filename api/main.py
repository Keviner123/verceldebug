import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def GetIfScoreHasBeenSet(user, song):
        connection = mysql.connector.connect(
            host='165.232.69.102',
            database='mgp',
            user='username',
            password='Oliver123'
        )



        cursor = connection.cursor()

        sql_select_query = """SELECT * FROM `rating` WHERE `name` = %s AND `song` = %s
        """
        # set variable in query
        cursor.execute(sql_select_query, (user,song))

        record = cursor.fetchall()
        if(len(record)>0):
            return(True)
        else:
            return(False)

def OpenSQLAndRunQuery(user, score, song):
    connection = mysql.connector.connect(
        host='165.232.69.102',
        database='mgp',
        user='username',
        password='Oliver123'
    )

    cursor = connection.cursor()

    scorehasbeenet = GetIfScoreHasBeenSet(user,song)

    if(scorehasbeenet):
        mySql_insert_query = """UPDATE rating set rating = %s WHERE name = %s and song = %s"""
        record = (score,user,song)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
    else:
        mySql_insert_query = """INSERT INTO rating (name, rating, song) 
        VALUES (%s, %s, %s) """
        record = (user,score,song)
        cursor.execute(mySql_insert_query, record)
        connection.commit()

def Average(lst):
    try:
        return sum(lst) / len(lst)
    except:
        return(0)

def CalculateAverage(index, rows) -> int:
    scores = []
    for x in rows:
        if(x[2] == index):
            scores.append(x[1])
    
    average = Average(scores)
    return('%.2f' % average)

def GetAverage():
    connection = mysql.connector.connect(
    host='165.232.69.102',
    database='mgp',
    user='username',
    password='Oliver123'
    )

    cursor = connection.cursor()
    sql_select_query = """SELECT * FROM `rating`
    """
    # set variable in query
    cursor.execute(sql_select_query)
    record = cursor.fetchall()

    returnstring = ""
    for x in range(8):
        returnstring += (CalculateAverage(x+1,record))+","
    return(returnstring)

@app.route('/setScore', methods=['POST'])
def update_record():
    content = request.json
    
    #Hacking safety, so only numbers between 1 and 10 can be submitted
    if(1 <= int(content["score"]) <= 10):
        OpenSQLAndRunQuery(request.remote_addr, content["score"], content["song"])
    return("")

@app.route('/getScore')
def update_record1():
    return(GetAverage())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')
