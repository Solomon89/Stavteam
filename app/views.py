from flask import render_template
from flask import jsonify, request
import pyodbc
from stavteam import app
import uuid
from flask import abort
import psycopg2

SERVER = ''
DATABASE = 'stavteamdb'
UID = 'stavuser'
PWD = 'password'

deleteInterval = 3600


def checkToNull(param):
    if str(param) == '':
        s = ' NULL,'
    elif param is None:
        s = ' NULL,'
    else:
        s = " '" + param + "',"
    return s


def execSQL(sql, param, needFeatch):
    cnxn = psycopg2.connect(dbname=DATABASE, user=UID,
                            password=PWD, host='localhost')
    cursor = cnxn.cursor()
    cursor.execute(sql)
    if needFeatch:
        rows = cursor.fetchall()
        cnxn.close()
        return rows
    else:
        try:
            ids = cursor.fetchone()[0]
        except:
            ids = None
        cnxn.commit()
        cnxn.close()
        return ids


def makeSession(userId):
    uid = str(uuid.uuid4())
    sql = '''INSERT INTO sessions (session,userID,loginTime)
     VALUES
           (\'''' + uid + '''\',
            ''' + str(userId) + ''',NOW()::timestamp)'''
    param = [uid, userId]
    execSQL(sql, param, False)
    return uid


def killSession(uid):
    sql = "delete FROM sessions where session='" + uid + "'"
    execSQL(sql, True, False)
    return True


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", user="Stavteam")


@app.route('/login', methods=['POST'])
def login():
    param = request.get_json()
    sql = "select users.* where LOGIN='%s'" % param['userName']
    rows = execSQL(sql, None, True)
    if len(rows) > 0:
        for row in rows:
            if row[2].strip() == param['userPass']:
                uid = makeSession(row[0])
                userInfo = {'FAM': row[4], 'IM': row[5], 'OT': row[6], 'SESSION': uid}
                return jsonify(userInfo)
        abort(401)
    else:
        abort(401)


@app.route('/logout', methods=['POST'])
def logout():
    param = request.get_json()
    if killSession(param['session']):
        return 'OK'
