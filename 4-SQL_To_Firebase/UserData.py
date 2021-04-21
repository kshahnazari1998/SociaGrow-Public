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

    def getnewuserdatafirestore(self):
        try:

            users_ref = self.firestoredb.collection(u"UserSettings").where(
                u"addedtodatabase", u"==", False
            )
            docs = users_ref.stream()
            for doc in docs:
                uid = u"{}".format(doc.to_dict()["uid"])
                count = self.SqlQueryExec(
                    "SELECT * FROM AppUsers where uid = %s", True, [uid]
                )
                if count == 0:
                    res = self.SqlQueryExec(
                        "INSERT INTO AppUsers (uid,Taskperday) VALUES (%s,40)",
                        False,
                        [uid],
                        True,
                    )
                    # Means Successful add to database
                    if res == 0:
                        addtofirebase = self.firestoredb.collection(
                            u"UserSettings"
                        ).document(uid)
                        addtofirebase.set({u"addedtodatabase": True}, merge=True)
        except:
            print("Something Failed in the function")

    def updateusers(self):
        try:
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
                        readfirebase = self.firestoredb.collection(
                            u"UserSettings"
                        ).document(uid)
                        docs = readfirebase.get()
                        Taskperday = u"{}".format(docs.to_dict()["Taskperday"])
                        res = self.SqlQueryExec(
                            "UPDATE AppUsers SET Taskperday=%s WHERE uid=%s",
                            False,
                            [Taskperday, uid],
                            True,
                        )
                        if res == 0:
                            break
                    except:
                        pass
        except:
            print("Error Occured in updateusers")


Taskdo = Updatemysqluserfromfirebase()
Taskdo.getnewuserdatafirestore()
Taskdo.updateusers()
print("success")
