from flask import render_template
from flask import jsonify, request
from stavteam import app
from flask import abort
from app import dbFunctions
from app import graph
from random import randint


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


@app.route('/lineInfo', methods=['POST'])
def getLineInfo():
    param = request.get_json()
    if dbFunctions.checkSession(param['session']):
        lineStatuses = dbFunctions.getlineStatus(param['lineId'])
        return jsonify(lineStatuses)
    else:
        abort(401)


@app.route('/map', methods=['POST'])
def getMap():
    param = request.get_json()
    if dbFunctions.checkSession(param['session']):
        recorders = dbFunctions.getRecorders()
        stations = dbFunctions.getStations()
        links = dbFunctions.getLinks()
        lines = {}
        for link in links:
            recorderIn = recorders[links[link]['idRecorderIn']]
            recorderOut = recorders[links[link]['idRecorderOut']]
            recorderInStation = stations[recorderIn['stationId']]
            recorderOutStation = stations[recorderOut['stationId']]
            coordInStation = {'lat': recorderInStation['lat'], 'lon': recorderInStation['lon']}
            coordOutStation = {'lat': recorderOutStation['lat'], 'lon': recorderOutStation['lon']}
            lines[link] = {'coordInStation': coordInStation,
                           'coordOutStation': coordOutStation}
        return jsonify({'lines': lines,
                        'stations': stations})
    else:
        abort(401)


@app.route('/graph/<int:event_id>')
def graphs(event_id):
    return render_template("graph.html")


@app.route('/getgraph/<int:event_id>/<int:id>/<path:typeGraph>')
def getgraph(event_id =0, id = 0,typeGraph = "analog"):
    way = dbFunctions.getEventFilePath(event_id)
    way = getWayToRecorderIdStatus()
    data = graph.GetGraphs(way,id,typeGraph)
    return  data


@app.route('/getgraph/<int:event_id>')
def getgraphInfo(event_id):
    way = dbFunctions.getEventFilePath(event_id)
    way = getWayToRecorderIdStatus()
    data = graph.GetGraphInfo(way)
    return jsonify(data)


def getWayToRecorderIdStatus():
    id = randint(0, 9)


    if(id == 0):
        return "static//Oscillogramm//04JUL205"
    elif(id== 1):
        return "static//Oscillogramm//04APR163"
    elif(id== 2):
        return "static//Oscillogramm//5DES2019"
    elif(id== 3):
        return "static//Oscillogramm//5DES20192"
    elif(id== 4):
        return "static//Oscillogramm//16DES2019"
    elif(id== 5):
        return "static//Oscillogramm//17DES2019"
    elif(id== 6):
        return "static//Oscillogramm//21DES2019"
    elif(id== 7):
        return "static//Oscillogramm//27DES2019"
    elif(id== 8):
        return "static//Oscillogramm//29NOVEM2019"
