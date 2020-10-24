from flask import render_template
from flask import jsonify, request
from stavteam import app
from flask import abort
from app import dbFunctions
from app import graph 



deleteInterval = 3600


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", user="Stavteam")


@app.route('/login', methods=['POST'])
def login():
    param = request.get_json()
    sql = '''SELECT * FROM public.users where users."userName"='%s' ''' % param['userName']
    rows = dbFunctions.execSQL(sql, None, True)
    if len(rows) > 0:
        for row in rows:
            if row[2].strip() == param['userPass']:
                uid = dbFunctions.makeSession(row[0])
                userInfo = {'FAM': row[4], 'IM': row[5], 'OT': row[6], 'SESSION': uid}
                return jsonify(userInfo)
        abort(401)
    else:
        abort(401)


@app.route('/logout', methods=['POST'])
def logout():
    param = request.get_json()
    if dbFunctions.killSession(param['session']):
        return 'OK'

@app.route('/map', methods=['POST'])
def getMap():
    param = request.get_json()
    if dbFunctions.checkSession(param['session']):
        lines=dbFunctions.getLines()
        stations=dbFunctions.getStations()
        return jsonify({'lines':lines,
                       'stations':stations})
    else:
        abort(401)

@app.route('/graph')
def getgraph():
        data = graph.GetGraphs("C:\\data\\04APR163")
        return  jsonify(data)