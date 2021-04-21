import mysql.connector
import pymysql
import time


class TaskBank:
    def __init__(self):
        for i in range(0, 5):
            try:
                self.__init_db()
                break
            except:
                print("Connection Failed to SQL")

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

    def __init_db(self):
        try:
            self.mydb = pymysql.connect(
                host="xxx", user="xxx", passwd="xxx", database="xxx"
            )

            self.mycursor = self.mydb.cursor()
        except:
            pass

    def filltaskbank(self):
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
            print("NEEEEEEEEEEEEEEEEEEEEEEEEEEEEXT user")
            try:
                for i in range(0, 100):
                    try:
                        count = self.SqlQueryExec(
                            "SELECT Liker,Liked,NumPosts,NumLiked FROM Likes WHERE (Scrapped=1 AND Publicornot=1 AND Followers>200 AND Following>100 AND (Following/Followers)>0.75 AND Posts>25 AND LIKER NOT IN (SELECT Account FROM Taskbank WHERE BINARY Account= BINARY Liker AND uid=%s) AND BINARY Liked IN (SELECT name FROM TargetAccounts WHERE uid=%s)) ORDER BY (NumLiked/NumPosts) DESC LIMIT 1",
                            True,
                            [uid, uid],
                        )
                        if count == 0:
                            break
                        else:
                            taskaccount = self.db[0]
                            targetacc = self.db[1]
                            numpost = self.db[2]
                            numliked = self.db[3]
                            likepercantage = round(numliked / numpost, 2)
                            if i % 3 == 0:
                                Task = "Follow"
                            if i % 3 == 1:
                                Task = "Like3"
                            if i % 3 == 2:
                                Task = "Likecomment"
                            self.SqlQueryExec(
                                "INSERT INTO Taskbank (uid,Account,Task,TargetAccount,Likepercentage) Values (%s,%s,%s,%s,%s)",
                                False,
                                [uid, taskaccount, Task, targetacc, likepercantage],
                                True,
                            )
                            print("And another one")
                    except:
                        pass

            except:
                print("Error In taskbank")


Taskdo = TaskBank()
Taskdo.filltaskbank()
print("success")
