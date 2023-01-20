import os, sys, time

"""
    DB User line
    ('username','userid','max_con','max_time','cooldown','mod_level')
          0         1        2         3          4          5
"""
class UserInfo:
    err:            bool
    err_msg:        str

    username:       str
    userid:         str
    max_con:        int
    max_time:       int
    cooldown:       int
    mod_level:      int
    

def setInfo(usr: str, uid: str, maxc: int, maxt: int, coold: int, modlvl: int) -> UserInfo:
    u = UserInfo
    
    u.username = usr
    u.userid = uid
    u.max_con = maxc
    u.max_time = maxt
    u.cooldown = coold
    u.mod_level = modlvl

    return u

class User():
    __db: str
    dbpath = "assets/users.db"
    def __init__(self) -> None:
        self.__db = self.__retrieveDB()


    def __retrieveDB(self) -> str:
        dbFile = open(self.dbpath, "r")
        db = dbFile.read()
        dbFile.close()
        self.__db = db
        return db

    def __parseLine(self, line: str) -> list:
        return line.replace("('", "").replace("')", "").replace("'", "").split(",")

    def find(self, uid: str) -> UserInfo:
        n = UserInfo
        usrs = open("assets/users.db", "r")
        users = usrs.read().split("\n")

        for line in users:
            if line == "": break
            parsed = self.__parseLine(line)
            
            if len(parsed) > 2:
                if str(parsed[1].strip()) == uid:
                    n = setInfo(parsed[0], parsed[1], int(parsed[2]), int(parsed[3]), int(parsed[4]), int(parsed[5]))
                    return n
        return setInfo("", "", 0, 0, 0, 0)

    def add(self, info: UserInfo) -> bool:
        try:
            dbFile = open(self.dbpath, "a")
            dbFile.write(f"('{info.username}','{info.userid}','{info.max_con}','{info.max_time}','{info.cooldown}','{info.mod_level}')\n")
            dbFile.close()
        except:
            return False
        return True

    def remove(self, uid: str) -> bool:
        new_db: str
        info = self.__resetInfo()
        if not f"'{uid}'" in self.__db:
            info.err = True
            info.err_msg = "[ X ] Error, Unable to find user!"
            return False

        for line in self.__db.split("\n"):
            if len(line) < 1: break
            parsed = self.__parseLine(line)
            if len(parsed) > 2:
                if parsed[1].strip() != uid:
                    new_db += line + "\n"

        self.__saveDB()
        return True

    def update(self, uid: str) -> bool:
        pass