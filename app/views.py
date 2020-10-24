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

@app.route('/graph/<int:event_id>')
def graphs(event_id):
    return render_template("graph.html")

@app.route('/getgraph/<int:event_id>/<int:id>/<path:typeGraph>')
def getgraph(event_id =0, id = 0,typeGraph = "analog"):
    way = getWayToRecorderIdStatus(0)
    data = graph.GetGraphs(way,id,typeGraph)
    return  data
@app.route('/getgraph/<int:event_id>')
def getgraphInfo(event_id):
    way = getWayToRecorderIdStatus(event_id)
    data = graph.GetGraphInfo(way)
    return jsonify(data)

def getWayToRecorderIdStatus(id):
    if(id%2 == 0):
        return "static\\Oscillogramm\\04JUL205"
    else:
        return "static\\Oscillogramm\\04APR163"
    