import InstaScraper
import mysql.connector
import pymysql
import time
from PremiumScraper import PremiumDataScraping as Pr


class TargetAccountStatus:
    def __init__(self):
        try:

            self.__init_db()
            self.PremiumScraper = Pr("xxx", "xxx", True, False)

        except:
            print(
                "Error in function init in Class Scraper. Big Error. Stopping Program"
            )
            time.sleep(50000)

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
        print("Couldn't Excecute " + Query + " in SqlQuery Function in Scraper Class")
        return -1

    def findalreadyscraped(self):
        try:
            while True:
                TargetScrapeUser = ""
                rowcount = self.SqlQueryExec(
                    "SELECT name FROM TargetAccounts WHERE Scraped=0 order by Rand() Limit 1",
                    True,
                )
                # Query Has failed
                if rowcount is -1:
                    # Error 1
                    print(
                        "Chain Error. Error In scrapeauser in class Scraper. Reason SqlQueryExec has failed. Error 1"
                    )
                    return -1
                if rowcount is 0:
                    # Finished Work
                    print("Finished")
                    return 0
                else:
                    # Check to see if we already have scraped the user.
                    TargetScrapeUser = self.db[0]
                    rowcount = self.SqlQueryExec(
                        "SELECT Liked FROM Likes WHERE Liked=%s",
                        True,
                        [TargetScrapeUser],
                    )
                    if rowcount == 0:
                        self.SqlQueryExec(
                            "UPDATE TargetAccounts SET Scraped=-1 WHERE name=%s",
                            True,
                            [TargetScrapeUser],
                            True,
                        )
                    else:
                        self.SqlQueryExec(
                            "UPDATE TargetAccounts SET Scraped=1 WHERE name=%s",
                            True,
                            [TargetScrapeUser],
                            True,
                        )
        except:
            print("Error in Findalreadyscraped")
            return -1

    def ScrapeTargetUsers(self):
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
                TargetScrapeUser = ""
                rowcount = self.SqlQueryExec(
                    "SELECT name FROM TargetAccounts WHERE Scraped=-1 order by Rand() Limit 1",
                    True,
                )
                # Query Has failed
                if rowcount is -1:
                    # Error 1
                    print(
                        "Chain Error. Error In scrapeauser in class Scraper. Reason SqlQueryExec has failed. Error 1"
                    )
                    continue
                if rowcount is 0:
                    continue
                else:
                    TargetScrapeUser = self.db[0]
                    rowcount = self.SqlQueryExec(
                        "SELECT Liked FROM Likes WHERE Liked=%s",
                        True,
                        [TargetScrapeUser],
                    )
                    if rowcount > 0:
                        self.SqlQueryExec(
                            "UPDATE TargetAccounts SET Scraped=1 WHERE name=%s",
                            True,
                            [TargetScrapeUser],
                            True,
                        )
                        continue
                    Targetdata = self.PremiumScraper.getuserdetails(TargetScrapeUser)
                    if Targetdata == "UserNotFound":
                        self.SqlQueryExec(
                            "UPDATE TargetAccounts SET Scraped=1 , Status=-1 WHERE name=%s",
                            True,
                            [TargetScrapeUser],
                            True,
                        )
                    elif Targetdata != -1 and hasattr(Targetdata, "__len__"):
                        # Means it is private
                        if Targetdata[1] == True:
                            self.SqlQueryExec(
                                "UPDATE TargetAccounts SET Scraped=1 , Status=-2 WHERE name=%s",
                                True,
                                [TargetScrapeUser],
                                True,
                            )
                        else:
                            self.PremiumScraper.addscrapeddata(
                                TargetScrapeUser, Targetdata
                            )
                            res = self.PremiumScraper.scraperlikes(TargetScrapeUser, 6)
                            if res == "Success":
                                self.SqlQueryExec(
                                    "UPDATE TargetAccounts SET Scraped=1 , Status=0 WHERE name=%s",
                                    True,
                                    [TargetScrapeUser],
                                    True,
                                )
                            # self.PremiumScraper.scraperfollowers(TargetScrapeUser)

        except:
            print("Error in Scrape Target Users")
            return -1


targ = TargetAccountStatus()

while True:
    for i in range(0, 3):
        targ.ScrapeTargetUsers()
        targ.findalreadyscraped()

print("Success")
