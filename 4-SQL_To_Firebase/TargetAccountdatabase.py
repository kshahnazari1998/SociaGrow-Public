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

    def getTargetAccountdatafirestore(self):
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
            for i in range(0, 5):
                try:
                    users_ref = self.firestoredb.collection(u"TargetAccounts").where(
                        u"uid", u"==", uid
                    )
                    docs = users_ref.stream()
                    count = self.SqlQueryExec(
                        "DELETE FROM TargetAccounts WHERE uid=%s ", False, [uid], True
                    )
                    for doc in docs:
                        targetname = u"{}".format(doc.to_dict()["Targetname"])
                        res = self.SqlQueryExec(
                            "INSERT INTO TargetAccounts (uid,name) VALUES (%s,%s)",
                            False,
                            [uid, targetname],
                            True,
                        )
                except:
                    pass


Taskdo = Updatemysqluserfromfirebase()
Taskdo.getTargetAccountdatafirestore()
print("success")
