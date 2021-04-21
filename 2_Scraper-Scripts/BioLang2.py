import pymysql
from googletrans import Translator
import time

translate_urls = [
    "translate.google.com",
    "translate.google.co.kr",
    "translate.google.at",
    "translate.google.de",
    "translate.google.ru",
    "translate.google.ch",
    "translate.google.fr",
    "translate.google.es",
]
translator = Translator(service_urls=translate_urls)
count = 0


class BioLang:
    def __init__(self):
        self.__init_db()
        self.capacity = 200
        self.counter = 0
        self.vpnnum = 0

    def __init_db(self):
        try:
            self.mydb = pymysql.connect(
                host="xxx", user="xxx", passwd="xxx", database="xxx"
            )

            self.mycursor = self.mydb.cursor()
        except:
            pass

    def getVpnnum(self):
        try:
            filef = open("CurrentVpnNumber.txt", "r")
            contents = filef.readlines()
            filef.close()
            vpnnumber = int(contents[0].strip())
            if vpnnumber is not self.vpnnum:
                print("Vpn Reset For BioLang!")
                self.counter = 0
                self.vpnnum = vpnnumber
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

    def manager(self):
        while True:
            try:
                if self.counter is self.capacity:
                    time.sleep(10)
                    self.getVpnnum()
                else:
                    rowcount = self.SqlQueryExec(
                        "select username,BioCleaned from publicprofiles WHERE ProfileLanguage IS NULL and BioCleaned is not NULL limit 1",
                        True,
                    )
                    if rowcount == 0:
                        print("No More To Scrape Pausing For a long time")
                        time.sleep(5000)
                    else:
                        user = self.db[0]
                        text = self.db[1]
                        if text == "NoBioHere":
                            self.SqlQueryExec(
                                "UPDATE publicprofiles SET ProfileLanguage='NNN' WHERE username=%s",
                                False,
                                [user],
                                True,
                            )
                        else:
                            lane = translator.detect(text)
                            lang = lane.lang
                            self.SqlQueryExec(
                                "UPDATE publicprofiles SET ProfileLanguage=%s WHERE username=%s",
                                False,
                                [lang, user],
                                True,
                            )
                            self.counter += 1
                            print(
                                "Added Bio Lang of user "
                                + user
                                + "To Database"
                                + " Counter is "
                                + str(self.counter)
                            )
            except:
                print("Error in manager function biolang")
                self.getVpnnum()
                time.sleep(30)


biolang = BioLang()
biolang.manager()