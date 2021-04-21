import mysql.connector
import pymysql
import firebase_admin
from firebase_admin import credentials, firestore
import time


class TaskGiver:
    def __init__(self):
        for i in range(0, 5):
            try:
                self.__init_db()
                break
            except:
                print("Connection Failed to SQL")
        for i in range(0, 5):
            try:
                self.__initfirebase_db()
                break
            except:
                print("Connection Failed to Firebase")

    def __init_db(self):
        try:
            self.mydb = pymysql.connect(
                host="xxx", user="xxx", passwd="xxx", database="xxx"
            )

            self.mycursor = self.mydb.cursor()
        except:
            pass

    def SqlQueryExec(self, Query, givecount=False, sqlinput=None, commitdatabase=False):
        for iter in range(0, 7):
            try:
                if sqlinput is None:
                    self.mycursor.execute(Query)
                else:
                    self.mycursor.execute(Query, sqlinput)
                if commitdatabase is True:
                    self.mydb.commit()
                if givecount is False:
                    return 0
                count = 0
                for self.db in self.mycursor:
                    count += 1
                return count
            except:
                time.sleep(1)
                self.__init_db()
        # If there was success in Query we shouldn't have reached this line
        print("Couldn't Excecute" + Query + " in SqlQuery Function in Scraper Class")
        return -1

    def __initfirebase_db(self):
        cred = credentials.Certificate("Firebasecredentials.json")
        defaultapp = firebase_admin.initialize_app(cred)
        self.firestoredb = firestore.client()

    def getcurdate(self):
        curdate = None
        for i in range(0, 6):
            try:
                self.mycursor.execute("SELECT curdate()")
                records = self.mycursor.fetchall()
                curdate = records[0]
                return curdate[0]
            except:
                time.sleep(1)
                pass
        return curdate

    def taskgive(self):

        curdate = self.getcurdate()
        if curdate == None:
            print("Can't get server time. Error in taskgive")
            return -1
        uidlist = []
        for i in range(0, 20):
            try:
                self.mycursor.execute("SELECT uid FROM AppUsers")
                records = self.mycursor.fetchall()
                for rows in records:
                    uidlist.append(rows[0])
                break
            except:
                self.__init_db()
        for uid in uidlist:
            try:
                count = self.SqlQueryExec(
                    "SELECT Taskperday FROM AppUsers WHERE uid=%s", True, [uid]
                )
                if count > 0:
                    numdailytask = self.db[0]
                    count = self.SqlQueryExec(
                        "SELECT count(Account) FROM Tasks WHERE uid=%s AND (Done=FALSE or DateAdded=%s)",
                        True,
                        [uid, curdate],
                    )
                    dailypresent = self.db[0]
                    tasktoadd = numdailytask - dailypresent
                    if tasktoadd < 0:
                        tasktoadd = 0
                        continue
                    if tasktoadd > 200:
                        tasktoadd = 200
                    for i in range(0, tasktoadd):
                        try:
                            count = self.SqlQueryExec(
                                "SELECT Account,Task,TargetAccount,Likepercentage FROM Taskbank WHERE (uid=%s AND Account NOT IN(SELECT Account FROM Tasks WHERE uid=%s) AND TargetAccount IN(SELECT name FROM TargetAccounts WHERE uid=%s)) ORDER BY Likepercentage DESC LIMIT 1",
                                True,
                                [uid, uid, uid],
                            )
                            if count == 0:
                                break
                            acc = self.db[0]
                            task = self.db[1]
                            target = self.db[2]
                            percen = self.db[3]
                            self.SqlQueryExec(
                                "INSERT INTO Tasks (uid,Account,Task,TargetAccount,Likepercentage,DateAdded) Values (%s,%s,%s,%s,%s,%s)",
                                False,
                                [uid, acc, task, target, percen, curdate],
                                True,
                            )
                        except:
                            pass

            except:
                pass


Taskdo = TaskGiver()
Taskdo.taskgive()
print("success")
