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
    sql = "delete FROM public.sessions where session='" + uid + "'"
    execSQL(sql, True, False)
    return True

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