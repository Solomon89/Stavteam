import psycopg2
import uuid

SERVER = '176.118.165.45'
DATABASE = 'stavteamdb'
UID = 'stavuser'
PWD = 'password'


def makeSession(userId):
    uid = str(uuid.uuid4())
    sql = '''INSERT INTO public.sessions(session, "userID", "loginTime")
     VALUES
           (\'''' + uid + '''\',
            ''' + str(userId) + ''',NOW()::timestamp)'''
    param = [uid, userId]
    execSQL(sql, param, False)
    return uid


def killSession(uid):
    sql = "delete FROM public.sessions where sessions.session='" + uid + "'"
    execSQL(sql, True, False)
    return True


def getlineStatus(lineId):
    sql = 'SELECT linestatus.* FROM public.linestatus where linestatus.line_id=' + str(
        lineId) + ' order by linestatus.id desc'
    lineStatuses = execSQL(sql, True, True)
    lineStatusesJSON = {}
    for lineStatus in lineStatuses:
        lineStatusesJSON[lineStatus[0]] = {'dateOfEvent': lineStatus[1],
                                           'fileName': lineStatus[2],
                                           'statusId': lineStatus[3],
                                           'lineId': lineStatus[4]}


def getLines(needFullInfo):
    sql = "SELECT line.* FROM public.line"
    lines = execSQL(sql, True, True)
    linesJSON = {}
    for line in lines:
        if needFullInfo:
            linesJSON[line[0]] = {'stationId': line[1],
                                  'name': line[2],
                                  'direction': line[3],
                                  'folder': line[4]}
        else:
            linesJSON[line[0]] = {'stationId': line[1],
                                  'name': line[2],
                                  'direction': line[3]}
    return linesJSON


def getStations(needFullInfo):
    sql = "SELECT station.* FROM public.station"
    stations = execSQL(sql, True, True)
    stationsJSON = {}
    for station in stations:
        if needFullInfo:
            stationsJSON[station[0]] = {'name': station[1],
                                        'lon': station[2],
                                        'lat': station[3],
                                        'ftpAdress': station[4],
                                        'ftpPassword': station[5]}
        else:
            stationsJSON[station[0]] = {'name': station[1],
                                        'lon': station[2],
                                        'lat': station[3]}
    return stationsJSON


def execSQL(sql, param, needFeatch):
    cnxn = psycopg2.connect(dbname=DATABASE, user=UID,
                            password=PWD, host=SERVER)
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


def checkToNull(param):
    if str(param) == '':
        s = ' NULL,'
    elif param is None:
        s = ' NULL,'
    else:
        s = " '" + param + "',"
    return s
