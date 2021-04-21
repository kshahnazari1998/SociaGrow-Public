import mysql.connector
import pymysql
from InstaScraper import InstaScraper
from datetime import datetime
import time
from VpnChanger import VpnChanger
import random


class Scraper:
    def __init__(self):
        try:

            self.__init_db()
            self.userconfigandinstascraper()

            if self.bottype == "useradmin":
                self.myvpnchanger = VpnChanger(self.numberofvpns)
                self.myvpnchanger.changevpn()
            self.logintime = 0
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

    def userconfigandinstascraper(self):
        try:
            filef = open("BotConfiguration.txt", "r")
            contents = filef.readlines()
            filef.close()
            self.botname = contents[0].strip()
            username = contents[1].strip().lower()
            if username == "none":
                username = ""
            password = contents[2].strip().lower()
            if password == "none":
                password = ""
            self.bottype = contents[3].strip().lower()
            displaychrome = contents[4].strip().lower()
            if displaychrome == "true":
                displaychrome = True
            else:
                displaychrome = False
            self.numberofvpns = int(contents[5].strip())
            self.myinstascraper = InstaScraper(
                "chromedriver.exe", username, password, "Cookies.txt", 3, displaychrome
            )

        except:
            print(
                "Error in function userconfigandinstascraper in Class Scraper. Big Error. Stopping Program"
            )
            time.sleep(50000)

    # if givecount is Trues means we want to get the number of rows returned.
    # Input means that we want data given to sql query to execute
    # If we want the database to get commited after Insert, Update or Delete then commitdatabase must be True
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

    # Selects a random user from database and scrapes it.
    # Returns 0 on Success
    def scrapeauser(self):
        try:

            curdate = self.getcurdate()
            ScrapeUser = ""
            rowcount = self.SqlQueryExec(
                "SELECT Liker FROM Likes WHERE (Scrapped=0 AND (DateFailed!=%s OR DateFailed IS NULL)) order by Rand() Limit 1",
                True,
                [curdate],
            )
            # Query Has failed
            if rowcount is -1:
                # Error 1
                print(
                    "Chain Error. Error In scrapeauser in class Scraper. Reason SqlQueryExec has failed. Error 1"
                )
            if rowcount is 0:
                # Error 2
                return self.normalscrapeauser()
            else:
                # Check to see if we already have scraped the user.
                ScrapeUser = self.db[0]
                rowcount1 = self.SqlQueryExec(
                    "SELECT username FROM privateprofiles where username=%s",
                    True,
                    [ScrapeUser],
                )
                rowcount2 = self.SqlQueryExec(
                    "SELECT username FROM publicprofiles where username=%s",
                    True,
                    [ScrapeUser],
                )

                # Means That user is in database and we don't need to add it
                if rowcount1 + rowcount2 != 0 and rowcount1 != -1 and rowcount2 != -1:
                    try:
                        if rowcount1 != 0:
                            rowcount1 = self.SqlQueryExec(
                                "SELECT Follower,Following,Posts FROM privateprofiles where username=%s",
                                True,
                                [ScrapeUser],
                            )
                            if rowcount1 == -1:
                                # Error 7
                                print("ERRRROR in ScrapeUser Error 7")
                            err = self.SqlQueryExec(
                                "UPDATE Likes SET Scrapped=True,Publicornot=False,Followers=%s,Following=%s,Posts=%s WHERE Liker=%s",
                                False,
                                [self.db[0], self.db[1], self.db[2], ScrapeUser],
                                True,
                            )
                            if err == -1:
                                print("ERRRROR in ScrapeUser Error 7")
                        else:
                            rowcount2 = self.SqlQueryExec(
                                "SELECT Followers,Following,Posts FROM publicprofiles where username=%s",
                                True,
                                [ScrapeUser],
                            )
                            if rowcount2 == -1:
                                # Error 8
                                print("ERRRROR in ScrapeUser Error 8")
                            err = self.SqlQueryExec(
                                "UPDATE Likes SET Scrapped=True,Publicornot=True,Followers=%s,Following=%s,Posts=%s WHERE Liker=%s",
                                False,
                                [self.db[0], self.db[1], self.db[2], ScrapeUser],
                                True,
                            )
                            if err == -1:
                                print("ERRRROR in ScrapeUser Error 8")
                        return 0
                    except:
                        print("Big error")

                result = self.myinstascraper.getuserdetails(ScrapeUser)
                # Check That a list is returned and it hasn't failed
                if result == "UserNotFound":
                    self.SqlQueryExec(
                        "SELECT FailedTimes FROM Likes WHERE Liker=%s",
                        True,
                        [ScrapeUser],
                    )

                    data = self.db[0]
                    if data is None or data == 0:
                        res = self.SqlQueryExec(
                            "UPDATE Likes SET FailedTimes=1,DateFailed=%s WHERE Liker=%s",
                            False,
                            [curdate, ScrapeUser],
                            True,
                        )
                        return -1
                    if data == 3:
                        suc = self.SqlQueryExec(
                            "DELETE FROM Likes WHERE Liker=%s",
                            False,
                            [ScrapeUser],
                            True,
                        )
                    else:
                        self.SqlQueryExec(
                            "UPDATE Likes SET FailedTimes=%s,DateFailed=%s WHERE Liker=%s",
                            False,
                            [data + 1, curdate, ScrapeUser],
                            True,
                        )
                    return -1
                if result != -1 and hasattr(result, "__len__"):
                    # Check to see if all the data are available
                    if len(result) == 7:
                        self.logintime = 0
                        sqlinput = []
                        for columns in result:
                            sqlinput.append(columns)

                        # Public Accounts
                        if result[1] == False:
                            sqlinput.pop(1)
                            sqlinput.append(False)
                            Curdate = datetime.now().date()
                            sqlinput.append(Curdate)
                            sqlinput.append("None")
                            Suc = self.SqlQueryExec(
                                "INSERT INTO publicprofiles (username,Verified,Posts,Followers,Following,Bio,Scrapped,DataUpdated,BotScraping) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                False,
                                sqlinput,
                                True,
                            )
                            self.SqlQueryExec(
                                "UPDATE Likes SET Scrapped=True,Publicornot=True,Followers=%s,Following=%s,Posts=%s WHERE Liker=%s",
                                False,
                                [sqlinput[3], sqlinput[4], sqlinput[2], ScrapeUser],
                                True,
                            )
                        # Private Accounts
                        else:
                            sqlinput.pop(2)
                            sqlinput.pop(1)
                            Curdate = datetime.now().date()
                            sqlinput.append(Curdate)
                            Suc = self.SqlQueryExec(
                                "INSERT INTO privateprofiles (username,Posts,Follower,Following,Bio,DateUpdated) Values (%s,%s,%s,%s,%s,%s)",
                                False,
                                sqlinput,
                                True,
                            )
                            self.SqlQueryExec(
                                "UPDATE Likes SET Scrapped=True,Publicornot=False,Followers=%s,Following=%s,Posts=%s WHERE Liker=%s",
                                False,
                                [sqlinput[2], sqlinput[3], sqlinput[1], ScrapeUser],
                                True,
                            )

                            print(
                                "Added "
                                + ScrapeUser
                                + " To Database : This Is from Liker"
                            )
                        if Suc is -1:
                            # Error 3
                            print("Some error ScrapeUser in ScraperClass Error 3")
                            return -1

                # 10 means Insta give try a few minutes later message
                elif result == -10:
                    # put back the failed user into database

                    # only useradmin has access to change the vpn
                    if self.bottype == "useradmin":
                        print("Changing VPN from Scrapeuser Function in Scraper Class")
                        self.myvpnchanger.changevpn()
                    else:
                        if self.logintime == 1:
                            time.sleep(1200)
                        elif self.logintime == 2:
                            time.sleep(3600)
                        else:
                            time.sleep(random.uniform(7200, 12000))
                        self.logintime += 1

                elif result == -1:
                    print("Scraping user " + ScrapeUser + "Failed")

                    return -1
        except:
            # Error 5
            print("Some Error in Scrapeuser in Scraper Class Error 5 ")

    def normalscrapeauser(self):
        try:

            ScrapeUser = ""
            rowcount = self.SqlQueryExec(
                "SELECT username FROM toscrape order by Rand() Limit 1", True
            )
            # Query Has failed
            if rowcount is -1:
                # Error 1
                print(
                    "Chain Error. Error In normalscrapeauser in class Scraper. Reason SqlQueryExec has failed. Error 1"
                )
            if rowcount is 0:
                # Error 2
                print(
                    "Error In normalscrapeauser in class Scrape. Nothing To scrape Continue. Error 2"
                )
                return -1
            else:

                # Check to see if we already have scraped the user.
                ScrapeUser = self.db[0]
                self.SqlQueryExec(
                    "DELETE FROM toscrape WHERE username=%s", False, [ScrapeUser], True
                )
                rowcount1 = self.SqlQueryExec(
                    "SELECT username FROM privateprofiles where username=%s",
                    True,
                    [ScrapeUser],
                )
                rowcount2 = self.SqlQueryExec(
                    "SELECT username FROM publicprofiles where username=%s",
                    True,
                    [ScrapeUser],
                )

                # Means That user is in database and we don't need to add it
                if rowcount1 + rowcount2 != 0 and rowcount1 != -1 and rowcount2 != -1:
                    return 0

                result = self.myinstascraper.getuserdetails(ScrapeUser)
                # Check That a list is returned and it hasn't failed
                if result is -3:
                    suc = self.SqlQueryExec(
                        "DELETE FROM toscrape WHERE username=%s",
                        False,
                        [ScrapeUser],
                        True,
                    )
                    return suc
                if result != -1 and hasattr(result, "__len__"):
                    # Check to see if all the data are available
                    if len(result) == 7:
                        sqlinput = []
                        for columns in result:
                            sqlinput.append(columns)

                        # Public Accounts
                        if result[1] == False:
                            sqlinput.pop(1)
                            sqlinput.append(False)
                            Curdate = datetime.now().date()
                            sqlinput.append(Curdate)
                            sqlinput.append("None")
                            Suc = self.SqlQueryExec(
                                "INSERT INTO publicprofiles (username,Verified,Posts,Followers,Following,Bio,Scrapped,DataUpdated,BotScraping) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                False,
                                sqlinput,
                                True,
                            )

                        # Private Accounts
                        else:
                            sqlinput.pop(2)
                            sqlinput.pop(1)
                            Curdate = datetime.now().date()
                            sqlinput.append(Curdate)
                            Suc = self.SqlQueryExec(
                                "INSERT INTO privateprofiles (username,Posts,Follower,Following,Bio,DateUpdated) Values (%s,%s,%s,%s,%s,%s)",
                                False,
                                sqlinput,
                                True,
                            )

                            print("Added " + ScrapeUser + " To Database")
                        if Suc is -1:
                            # Error 3
                            print("Some error normalScrapeUser in ScraperClass Error 3")
                            return -1

                # 10 means Insta give try a few minutes later message
                elif result == -10:
                    # put back the failed user into database
                    self.SqlQueryExec(
                        "INSERT INTO toscrape (username) Values (%s)",
                        False,
                        [ScrapeUser],
                        True,
                    )

                    # only useradmin has access to change the vpn
                    if self.bottype == "useradmin":
                        print("Changing VPN from Scrapeuser Function in Scraper Class")
                        self.myvpnchanger.changevpn()
                    else:
                        time.sleep(120)

                elif result == -1:
                    print("Scraping user " + ScrapeUser + "Failed")
                    self.SqlQueryExec(
                        "INSERT INTO toscrape (username) Values (%s)",
                        False,
                        [ScrapeUser],
                        True,
                    )
                    return -1
        except:
            # Error 5
            print("Some Error in normalScrapeuser in Scraper Class Error 5 ")

    def scraperfollowings(self):
        try:
            random_num = random.randint(1, 21)
            if random_num <= 14:
                rowcount = self.SqlQueryExec(
                    "SELECT username FROM publicprofiles WHERE Followers >= 100000 and Following != 0 and Scrapped != 1 Limit 1",
                    True,
                )
            elif random_num > 14 and random_num < 18:
                rowcount = self.SqlQueryExec(
                    "SELECT username FROM publicprofiles WHERE Followers < 100000 and Followers > 25000 and Following != 0 and Scrapped != 1 Limit 1",
                    True,
                )
            elif random_num >= 18 and random_num < 20:
                rowcount = self.SqlQueryExec(
                    "SELECT username FROM publicprofiles WHERE Followers <= 25000 and Followrs >= 5000 and Following != 0 & Scrapped != 1 Limit 1",
                    True,
                )
            else:
                rowcount = self.SqlQueryExec(
                    "SELECT username FROM publicprofiles WHERE Followers < 5000 and Following != 0 and Scrapped != 1 Limit 1",
                    True,
                )
            if rowcount is 0:
                # Error1
                print(
                    "Error in function scraperfollowings class Scraper. Nothing To scrape. Error1"
                )
                return -1
            elif rowcount is -1:
                # Error2
                print("Error in function scraperfollowings class Scraper. Error2")
                return -1
            else:
                try:
                    ScrapeUser = self.db[0]
                    self.SqlQueryExec(
                        "UPDATE publicprofiles SET BotScraping=%s , DataUpdated=%s WHERE username=%s",
                        False,
                        [self.botname, datetime.now().date(), ScrapeUser],
                        True,
                    )
                    Followerslist = self.myinstascraper.getuserfollowing(ScrapeUser)
                    if Followerslist != -1:
                        for followings in Followerslist:
                            rowcount = self.SqlQueryExec(
                                "SELECT username FROM toscrape where username=%s",
                                True,
                                [followings],
                            )
                            if rowcount == 0:
                                self.SqlQueryExec(
                                    "INSERT INTO toscrape (username) Values (%s)",
                                    False,
                                    [followings],
                                    True,
                                )
                        self.SqlQueryExec(
                            "UPDATE publicprofiles SET Scrapped=True WHERE username=%s",
                            False,
                            [ScrapeUser],
                            True,
                        )
                    else:
                        print("Some Error When Scrapping")
                        return -1
                except Exception as err:
                    # Error2
                    print(
                        "Some Problem in function scraper followings in class Scraper. Error2. with some error printing"
                    )
                    print(str(err))
        except:
            # Error 3
            print(
                "Some Problem in function scraper followings in class Scraper. Error3"
            )

    def premiumScrapeFollower(self):
        try:
            rowcount = self.SqlQueryExec(
                "SELECT AccountFollowed FROM PremiumFollowedHistory Where Scrapped is NULL LIMIT 1",
                True,
            )
            if rowcount is 0:
                print("PremiumScrapeFollower From Scraper, No more to Scrape.")
                return 2
            if rowcount is -1:
                time.sleep(60)
                return -1
            ScrapeUser = self.db[0]
            count1 = self.SqlQueryExec(
                "SELECT username FROM privateprofiles Where username=%s",
                True,
                [ScrapeUser],
            )
            count2 = self.SqlQueryExec(
                "SELECT username FROM publicprofiles Where username=%s",
                True,
                [ScrapeUser],
            )
            if count1 is -1 or count2 is -1:
                # Error 1
                print("Error in premiumscraper followers in class Scraper. Error 1")
                return -1
            else:
                if (count1 + count2) == 0:
                    result = self.myinstascraper.getuserdetails(ScrapeUser)
                    if result is -3:
                        suc = self.SqlQueryExec(
                            "DELETE FROM PremiumFollowedHistory WHERE AccountFollowed=%s",
                            False,
                            [ScrapeUser],
                            True,
                        )
                        return suc
                    if result != -1 and hasattr(result, "__len__"):
                        if len(result) == 7:
                            sqlinput = []
                            for columns in result:
                                sqlinput.append(columns)
                            # Public Accounts
                            if result[1] == False:
                                sqlinput.pop(1)
                                sqlinput.append(False)
                                Curdate = datetime.now().date()
                                sqlinput.append(Curdate)
                                sqlinput.append("None")
                                Suc = self.SqlQueryExec(
                                    "INSERT INTO publicprofiles (username,Verified,Posts,Followers,Following,Bio,Scrapped,DataUpdated,BotScraping) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    False,
                                    sqlinput,
                                    True,
                                )
                            # Private Accounts
                            else:
                                sqlinput.pop(2)
                                sqlinput.pop(1)
                                Curdate = datetime.now().date()
                                sqlinput.append(Curdate)
                                Suc = self.SqlQueryExec(
                                    "INSERT INTO privateprofiles (username,Posts,Follower,Following,Bio,DateUpdated) Values (%s,%s,%s,%s,%s,%s)",
                                    False,
                                    sqlinput,
                                    True,
                                )
                        if Suc is -1:
                            # Error 2
                            print(
                                "Error in premiumscraper followers in class Scraper. Error 2"
                            )
                            return -1

                        self.SqlQueryExec(
                            "UPDATE PremiumFollowedHistory SET Scrapped=True WHERE AccountFollowed=%s",
                            False,
                            [ScrapeUser],
                            True,
                        )

                    elif result == -10:
                        if self.bottype == "useradmin":
                            print(
                                "Changing VPN from Scrapeuser Function in Scraper Class"
                            )
                            self.myvpnchanger.changevpn()
                        else:
                            time.sleep(120)
                            return -1

                    else:
                        # Error 3
                        print(
                            "Error in premiumscraper followers in class Scraper. Error 3"
                        )
                        return -1
                else:
                    self.SqlQueryExec(
                        "UPDATE PremiumFollowedHistory SET Scrapped=True WHERE AccountFollowed=%s",
                        False,
                        [ScrapeUser],
                        True,
                    )
        except:
            # Error 4
            print("Error in premiumscraper followers in class Scraper. Error 4")
            return -1

    # Chooses to use scrapeuser or scrapeFollowing.
    def classmanager(self):

        FailCount = 0
        if self.bottype == "user" or self.bottype == "useradmin":
            while True:
                result = self.scrapeauser()
                # Means Some Function has Failed
                if result is -1:
                    print("Chain Error in function classmanager in class Scraper")
                    FailCount += 1
                    time.sleep(30)
                else:
                    FailCount = 0
                # After Few Fails Do a Reset.
                if FailCount > 0 and FailCount % 3 == 0 and self.bottype == "useradmin":
                    print(
                        "VpnChange And Browser Reset due to consecutive errors in function classmanager in class Scraper"
                    )
                    self.myvpnchanger.changevpn()
                    time.sleep(10)
                    self.myinstascraper.resetbrowser()

                if FailCount > 0 and FailCount % 3 == 0 and self.bottype == "user":
                    print("Browser Reset")
                    self.myinstascraper.resetbrowser()

                if FailCount == 9:
                    print("Pausing Program Something big in class manager")
                    time.sleep(30000)
                    break

                time.sleep(random.uniform(15, 100))

        elif self.bottype == "premiumuser":
            while True:
                success = self.premiumScrapeFollower()
                time.sleep(1)
                if success == 2:
                    print("Nothing to scrape")
                    time.sleep(1800)

                if success == -1:
                    print("Error Going To Sleep")
                    FailCount += 1
                    time.sleep(30)
                else:
                    FailCount = 0

                if FailCount > 0 and FailCount % 3 == 0:
                    print("Browser Reset")
                    self.myinstascraper.resetbrowser()

                if FailCount == 9:
                    print("Pausing Program Something big in class manager")
                    time.sleep(30000)

        else:
            while True:
                success = self.scraperfollowings()
                if success == -1:
                    print("Error Scraping Followers")
                    FailCount += 1
                else:
                    FailCount = 0
                if FailCount > 0 and FailCount % 3 == 0:
                    print("Resetting Browser")
                    self.myinstascraper.resetbrowser()

                if FailCount == 9:
                    print("Pausing Program Something big in class manager")
                    time.sleep(30000)
                time.sleep(10)


SCP = Scraper()
SCP.classmanager()
