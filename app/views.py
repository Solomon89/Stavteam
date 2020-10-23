from flask import render_template
from flask import jsonify, request
import pyodbc
from stavteam import app
import uuid
from flask import abort

SERVER = ''
DATABASE = ''
UID = ''
PWD = ''

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
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + SERVER + ';DATABASE=' + DATABASE + ';UID=' + UID + ';PWD=' + PWD)
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


def makeSession(userId, LPU):
    uid = str(uuid.uuid4())
    sql = '''INSERT INTO [reanim].[dbo].[sessions]
           ([SESSION]
           ,[userID]
           ,[LPU]
           ,[loginTime])
     VALUES
           (\'''' + uid + '''\',
            ''' + str(userId) + ''',
            ''' + str(LPU) + ''',GETDATE())'''
    param = [uid, userId, LPU]
    execSQL(sql, param, False)
    return uid


def killSession(uid):
    sql = "delete FROM [reanim].[dbo].[sessions] where [SESSION]=N'" + uid + "'"
    execSQL(sql, True, False)
    return True


def killExpiredSessions(interval):
    sql = '''DELETE FROM [reanim].[dbo].[sessions]
               where DATEDIFF(SECOND,[reanim].[dbo].[sessions].loginTime,GETDATE())>''' + str(interval)
    execSQL(sql, True, False)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", user="Stavteam")


@app.route('/login', methods=['POST'])
def login():
    param = request.get_json()
    sql = "select users.*,LPU.nameLPU from users left join LPU on LPU.ID=users.LPU where LOGIN='%s'" % param['userName']
    rows = execSQL(sql, None, True)
    if len(rows) > 0:
        for row in rows:
            if row[6].strip() == param['userPass']:
                uid = makeSession(row[0], row[4])
                userInfo = {'FAM': row[1], 'IM': row[2], 'OT': row[3], 'SESSION': uid, 'LPU': row[7]}
                return jsonify(userInfo)
        abort(401)
    else:
        abort(401)


@app.route('/logout', methods=['POST'])
def logout():
    param = request.get_json()
    if killSession(param['session']):
        return 'OK'
