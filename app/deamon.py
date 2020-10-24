import threading
import time
from app import dbFunctions
import ftplib
import os
import re


def _is_ftp_dir(ftp, name, guess_by_extension=True):
    if guess_by_extension is True:
        if len(name) >= 4:
            if name[-4] == '.':
                return False
    try:
        ftp.cwd(name.lstrip())
        return True
    except ftplib.error_perm as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False


def _download_ftp_file(station, ftp, name, dest, overwrite):
    dest = dest.split('/')[-1]
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftp.retrbinary("RETR {0}".format(name), f.write)
            if dest[-4:] == '.cfg':
                dbFunctions.newEvent(station, dest[:-4])
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("already exists: {0}".format(dest))


def _file_name_match_patern(pattern, name):
    if pattern is None:
        return True
    else:
        return bool(re.match(pattern, name))


def _mirror_ftp_dir(station, ftp, name, overwrite, guess_by_extension, pattern):
    for item in ftp.nlst(ftp.pwd()):
        if _is_ftp_dir(ftp, item, guess_by_extension):
            _mirror_ftp_dir(ftp, item, overwrite, guess_by_extension, pattern)
        else:
            if _file_name_match_patern(pattern, name):
                _download_ftp_file(station, ftp, item, item, overwrite)
            else:
                pass


def download_ftp_tree(station, ftp, path, destination, pattern=None, overwrite=False, guess_by_extension=True):
    path = path.lstrip("/")
    original_directory = os.getcwd()
    os.chdir(destination)
    _mirror_ftp_dir(station,
                    ftp,
                    path,
                    pattern=pattern,
                    overwrite=overwrite,
                    guess_by_extension=guess_by_extension)
    os.chdir(original_directory)


def timerKillSessions(interval):
    data = threading.local()
    while True:
        time.sleep(interval)
        dbFunctions.killExpiredSessions(interval)


def timerCheckFTP(interval):
    stations = dbFunctions.getStations(True)
    for station in stations:
        ftpAdress = stations[station]['ftpAdress']
        ftpUser = stations[station]['ftpUser']
        ftpPass = stations[station]['ftpPassword']
        ftp = ftplib.FTP(ftpAdress, ftpUser, ftpPass)
        ftp.login(ftpUser, ftpPass)
        remote_dir = ".."  # Путь к файлам на сервере FTP
        local_dir = r'путь к локальному хранилищу'
        download_ftp_tree(station, ftp, remote_dir, local_dir, overwrite=False, guess_by_extension=True)


deleteInterval = 3600
deamonDeleteSession = threading.Thread(target=timerKillSessions, name="killSessions", args=(deleteInterval,),
                                       daemon=True)
deamonDeleteSession.start()
##Настройка FTP
##checkFTPInterval = 600
##deamonCheckFTP = threading.Thread(target=timerCheckFTP, name="checkFTP", args=(checkFTPInterval,), daemon=True)
##deamonCheckFTP.start()
