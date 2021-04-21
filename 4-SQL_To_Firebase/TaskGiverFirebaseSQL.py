import mysql.connector
import pymysql
import firebase_admin
from firebase_admin import credentials, firestore
import time


class Updatemysqluserfromfirebase:
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

    def pushTasksfirestore(self):
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
                for tries in range(0, 10):
                    try:
                        self.mycursor.execute(
                            "SELECT Account,Task,TargetAccount,Likepercentage FROM Tasks WHERE Done=0 AND uid=%s AND Addedtobase=0",
                            [uid],
                        )
                        break
                    except:
                        pass
                records = self.mycursor.fetchall()
                for rows in records:
                    try:
                        Account = rows[0]
                        Task = rows[1]
                        TargetAccount = rows[2]
                        Likepercentage = rows[3]
                        Tasks_ref = self.firestoredb.collection(u"Tasks").add(
                            {
                                u"Account": Account,
                                u"Done": False,
                                u"Task": Task,
                                u"uid": uid,
                                u"TargetAccount": TargetAccount,
                                u"Likepercentage": Likepercentage,
                            }
                        )
                        self.SqlQueryExec(
                            "UPDATE Tasks SET Addedtobase=1 WHERE (uid=%s AND Account=%s)",
                            False,
                            [uid, Account],
                            True,
                        )
                    except:
                        # Error 1
                        print("Error 1 in pushtargetaccounterrorfirestore")

            except:
                pass

    def gettasksdone(self):
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
                users_ref = (
                    self.firestoredb.collection(u"Tasks")
                    .where(u"uid", u"==", uid)
                    .where(u"Done", u"==", True)
                )
                docs = users_ref.stream()
                for doc in docs:
                    acc = u"{}".format(doc.to_dict()["Account"])

                    res = self.SqlQueryExec(
                        "UPDATE Tasks SET Done=1 WHERE (uid=%s AND Account=%s)",
                        False,
                        [uid, acc],
                        True,
                    )
                    if res == 0:
                        self.firestoredb.collection(u"Tasks").document(doc.id).delete()

            except:
                print("Unexpected Error")


Taskdo = Updatemysqluserfromfirebase()
Taskdo.gettasksdone()
Taskdo.pushTasksfirestore()

print("success")
