from instapy import InstaPy
from explicit import waiter, XPATH
from instapy import commenters_util
import time
import traceback
import itertools
import re
import mysql.connector
import pymysql
import time
import random
from datetime import datetime


class PremiumDataScraping:
    def __init__(self, username, password, loginornot=True, headless=True):
        self.username = username.lower()
        self.password = password
        self.headless = headless
        self.session = InstaPy(
            username=username, password=password, headless_browser=headless
        )
        time.sleep(5)

        if loginornot == True:
            self.session.login()
        self.driver = self.session.browser

        self.mydb = pymysql.connect(
            host="xxx", user="xxx", passwd="xxx", database="xxx"
        )
        self.mycursor = self.mydb.cursor()

    def RestartBrowser(self):
        self.driver.quit()
        time.sleep(5)
        del self.session
        self.session = InstaPy(
            username=self.username,
            password=self.password,
            headless_browser=self.headless,
        )
        time.sleep(5)
        self.session.login()
        self.driver = self.session.browser

    def __init_db(self):
        self.mydb = pymysql.connect(
            host="www.sociagrow.com",
            user="sociagro_root",
            passwd="vN@zOr~0lt~M",
            database="sociagro_ourdatabase",
        )
        self.mycursor = self.mydb.cursor()

    # Function used in getuserdetails to remove emoji
    def __strip_emoji(self, text):
        RE_EMOJI = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
        return RE_EMOJI.sub(r"", text)

    # Gets basic information like bio, posts , followers , following , privatepublic and verified
    # Returns -1 on failiure
    # Todo : if result -10 means we have scrapped to much and we need to sleep the account or move to another account
    def getuserdetails(self, targetaccount):
        try:
            targetaccount = targetaccount.lower()
            # Go To user profile
            linkprofile = "https://www.instagram.com/" + targetaccount
            self.driver.get(linkprofile)
            # Check if Account exists, is public or private
            # Wait for the page to load checked by search bar
            time.sleep(3)
            if self.driver.find_elements_by_xpath("/html/body/div/div[1]/div/div/h2"):
                if (
                    self.driver.find_element_by_xpath(
                        "/html/body/div/div[1]/div/div/h2"
                    ).text.strip()
                    == "Sorry, this page isn't available."
                ):
                    return "UserNotFound"
            else:
                # Get Account Data
                # Check if Data is Private or public
                PrivateOrNot = False
                if self.driver.find_elements_by_xpath(
                    '// *[ @ id="react-root"] / section / main / div / div[2] / article / div[1]'
                ):
                    if (
                        self.driver.find_element_by_xpath(
                            '// *[ @ id="react-root"] / section / main / div / div[2] / article / div[1]'
                        ).text.strip()
                        != ""
                    ):
                        PrivateOrNot = True
                if self.driver.find_elements_by_xpath(
                    '// *[ @ id="react-root"] / section / main / div / div / article / div[1]'
                ):
                    if (
                        self.driver.find_element_by_xpath(
                            '// *[ @ id="react-root"] / section / main / div / div / article / div[1]'
                        ).text.strip()
                        != ""
                    ):
                        PrivateOrNot = True
                # Get the profile data
                ss = waiter.find_element(
                    self.driver,
                    '//*[@id="react-root"]/section/main/div/header/section',
                    by=XPATH,
                )
                ss = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section'
                )
                # Splits The Recieved Data
                AccountData = ss.text.splitlines()
                # Checking if the account is verified or not
                lines = [line for line in AccountData]
                verified = True if lines[1] == "Verified" else False
                if verified:
                    lines.pop(1)
                # Sometimes Shows that the people you have followed are following the person in that box
                # We don't want to have that
                if "Followed by" in lines[len(lines) - 1]:
                    lines.pop(len(lines) - 1)
                # See if user has no NickName and no bio
                if len(lines) == 5:
                    lines.append("NoBioHere")

                # remove the posts word from the string, special case the word is post for 1 post.
                # , is shown in the posts when its a 4 digit number like 4,212
                Postcount = lines[2].replace("posts", "").strip()
                Postcount = Postcount.replace("post", "")
                Postcount = Postcount.replace(",", "")

                # just like Post Count, Followers and Following words are removed
                Followerscount = lines[3].replace("followers", "").strip()
                Followerscount = Followerscount.replace("follower", "").strip()
                Followerscount = Followerscount.replace(",", "")
                Followingcount = lines[4].replace("following", "").strip()
                Followingcount = Followingcount.replace(",", "")

                # We need to put a int into database so we convert the text to number
                if "k" in Followerscount:
                    Followerscount = (
                        float(Followerscount[: len(Followerscount) - 1]) * 1000
                    )
                elif "m" in Followerscount:
                    Followerscount = (
                        float(Followerscount[: len(Followerscount) - 1]) * 1000000
                    )
                if "k" in Postcount:
                    Postcount = float(Postcount[: len(Postcount) - 1]) * 1000
                Followerscount = int(Followerscount)
                Followingcount = int(Followingcount)
                Postcount = int(Postcount)

                # Bio text is all that remains
                BioText = ""
                for x in lines[5:]:
                    BioText = BioText + x + "----"
                # remove the emoji from bio
                BioText = self.__strip_emoji(BioText)

                # Returns All These Parameters
                return (
                    targetaccount,
                    PrivateOrNot,
                    verified,
                    Postcount,
                    Followerscount,
                    Followingcount,
                    BioText,
                )

        except Exception as err:
            # if we are directed to the login page then a Vpn Change is required
            url = self.driver.current_url
            if url == "https://www.instagram.com/accounts/login/":
                return -10

            # for other errors this is it.
            if "list" in str(err):
                traceback.print_exc()
                print("Stop")
            traceback.print_exc()
            print(str(err))
            return -1

        # Todo : pass result to this function

    def addscrapeddata(self, ScrapeUser, result):
        # We pass the getuser details to this function to add
        # result=self.getuserdetails(ScrapeUser)
        try:
            if result != -1 and hasattr(result, "__len__"):
                if len(result) == 7:
                    cresult = []
                    for x in result:
                        cresult.append(x)
                    # Public Accounts
                    if result[1] == False:
                        cresult.pop(1)
                        cresult.append(False)
                        Curdate = datetime.now()
                        cresult.append(Curdate)
                        cresult.append("None")
                        Sqlquery = "REPLACE INTO publicprofiles (username,Verified,Posts,Followers,Following,Bio,Scrapped,DataUpdated,BotScraping) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        self.mycursor.execute(Sqlquery, cresult)
                        self.mydb.commit()
                    # Private Accounts
                    else:
                        cresult.pop(2)
                        cresult.pop(1)
                        Curdate = datetime.now()
                        cresult.append(Curdate)
                        Sqlquery = "REPLACE INTO privateprofiles (username,Posts,Follower,Following,Bio,DateUpdated) Values (%s,%s,%s,%s,%s,%s)"
                        self.mycursor.execute(Sqlquery, cresult)
                        self.mydb.commit()
            elif result == -10:
                print("We need to sleep")
                # add the code here

            elif result == -1:
                print("Scraping user failed")
                return -1
        except:
            return -1

    # Function used in getuserliked
    # Which includes scrolling and elemnt tags
    def __userlikes(self):
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div[2]/button/span'
            ).click()
            time.sleep(2)

            # here, you can see user list you want.
            # you have to scroll down to download more data from instagram server.
            # loop until last element with users table view height value.

            users = []
            try:
                height = self.driver.find_element_by_xpath(
                    "/html/body/div[4]/div/div[2]/div/div"
                ).value_of_css_property("padding-top")
            except:
                print("This is error fuck it")
            match = False
            trynum = 0
            while match == False:

                lastHeight = height

                # step 1
                try:
                    elements = self.driver.find_elements_by_xpath("//*[@id]/div/a")
                except:
                    print("Step1 FAIL")

                # step 2
                try:
                    for element in elements:
                        if element.get_attribute("title") not in users:
                            nametoadd = element.get_attribute("title")
                            if nametoadd not in users:
                                users.append(nametoadd)
                            if len(users) > 300:
                                return users
                except:
                    print("Step2 FAIL")

                # step 3
                try:
                    self.driver.execute_script(
                        "return arguments[0].scrollIntoView();", elements[-1]
                    )
                    time.sleep(3)
                except:
                    print("Step3 FAIL")

                # step 4
                try:
                    height = self.driver.find_element_by_xpath(
                        "/html/body/div[4]/div/div[2]/div/div"
                    ).value_of_css_property("padding-top")
                    if lastHeight == height:
                        trynum += 1
                    if trynum == 5:
                        print("Try Num Failed")
                        match = True
                except:
                    print("Step4 FAIL")

                if len(users) > 300:
                    print("page success")
                    return users
            print("page success")
            return users
        except:
            if len(users) > 200:
                print("page success")
                return users
            return -1

    # Function to get users who liked the posts of that user
    # account name is target user and num posts is the posts which we are going to scrape
    # if 1 returned means the posts are videos
    # if 2 returned means the target account is too big (>10000 likes)
    # if -1 means failed
    # if list returned means everything is fine
    # The list is a list containing num posts of list which is for every post
    def __getuserliked(self, accountname, numposts):
        try:
            users = []
            LikedPostsLinks = commenters_util.get_photo_urls_from_profile(
                self.driver,
                accountname,
                21,
                False,
            )
            PostCounted = 0
            PostsGot = 0
            while PostCounted is not numposts and (
                PostsGot is not 21 or PostsGot is not len(LikedPostsLinks)
            ):
                self.driver.get(LikedPostsLinks[PostsGot])
                time.sleep(5)
                if self.driver.find_elements_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div[2]/button/span'
                ):
                    LikeButton = waiter.find_element(
                        self.driver,
                        '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div[2]/button/span',
                        by=XPATH,
                    )
                    LikeCount = LikeButton.text.replace(",", "")
                    if int(LikeCount) > 1000000000:
                        print("Too big of account")
                        return 2
                    tried = 0
                    # Try 2-3 times
                    while True:
                        usersliked = self.__userlikes()
                        if usersliked == -1:
                            print("Error Occurred Trying again error 1")
                            time.sleep(10)

                            self.driver.get(LikedPostsLinks[PostsGot])
                            tried += 1
                        elif (
                            len(usersliked) < int(LikeCount) * 0.90 - 5
                            and len(usersliked) < 200
                        ):
                            print("Error Occurred Trying again error 2")
                            time.sleep(10)
                            self.driver.get(LikedPostsLinks[PostsGot])
                            tried += 1
                        else:
                            users.append(usersliked)
                            PostCounted += 1
                            time.sleep(3)
                            break
                        if tried == 5:
                            print("Can't get likes for big reason")
                            break
                    PostsGot += 1

                if self.driver.find_elements_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]'
                ):
                    Viewcount = waiter.find_element(
                        self.driver,
                        '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]',
                        by=XPATH,
                    )

                    if "view" in Viewcount.text.lower():
                        PostsGot += 1
                        print("Viewgot")

                if PostCounted == numposts:
                    return users
            if PostsGot > 0 and PostCounted == 0:
                print("Probably the posts are all videos")
                return 1
            else:
                return users
        except:
            print("Something went wrong big")
            return -1

    # Call this function to get the likes of someone and add to database
    # Returns Success if done completly
    # Todo : Write the numpost = 0
    def scraperlikes(self, accountname, numposts):
        try:
            results = self.__getuserliked(accountname, numposts)
            if results != -1:
                if results == 1 or results == 2:
                    return "Success"
                else:
                    numpost = len(results)
                    if numpost == 0:
                        return -1
                    else:
                        Lis = []
                        for x in results:
                            Lis += x
                        freq = {}
                        for item in Lis:
                            if item in freq:
                                freq[item] += 1
                            else:
                                freq[item] = 1
                        Curdate = datetime.now()

                        # New Version
                        SqlData = []
                        for k, v in freq.items():
                            SqlData.append((accountname, k, numpost, v, Curdate))
                        for i in range(0, 7):
                            try:
                                Sqlquery = "INSERT INTO Likes (Liked,Liker,NumPosts,NumLiked,DateUpdate) Values (%s,%s,%s,%s,%s)"
                                self.mycursor.executemany(Sqlquery, SqlData)

                                self.mydb.commit()
                                print("Success in adding to database user")
                                break
                            except Exception as e:
                                print(e)
                                self.__init_db()
                                print("Error in adding data")

                        # Old Version Adding one by one
                        """
                        for k, v in freq.items():
                            for i in range(0, 7):
                                try:
                                    SqlData = [accountname, k,
                                               numpost, v, Curdate]
                                    Sqlquery = "INSERT INTO Likes (Liked,Liker,NumPosts,NumLiked,DateUpdate) Values (%s,%s,%s,%s,%s)"
                                    self.mycursor.execute(Sqlquery, SqlData)
                                    self.mydb.commit()
                                    break
                                except:
                                    time.sleep(1)
                                    self.__init_db()
                                    time.sleep(1)
                        """

                        return "Success"
            else:
                print("An error In getuserliked Function")
                return -1
        except:
            print("An error In getuserliked Function")
            return -1

    # if no hashtags are found 2 is returned.
    def __getuserusedhashtag(self, targetaccount):
        try:
            hashtags = []

            LikedPostsLinks = commenters_util.get_photo_urls_from_profile(
                self.driver,
                targetaccount,
                50,
                False,
            )
            for i in range(0, 5):
                LikedPostsLinks2 = commenters_util.get_photo_urls_from_profile(
                    self.driver,
                    targetaccount,
                    50,
                    False,
                )
                Linksgot = len(LikedPostsLinks2)
                if Linksgot > len(LikedPostsLinks):
                    LikedPostsLinks = LikedPostsLinks2

            for x in LikedPostsLinks:
                for i in range(0, 2):
                    try:
                        time.sleep(2)
                        self.driver.get(x)
                        time.sleep(3)
                        ss = waiter.find_element(
                            self.driver,
                            "/html/body/div[1]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span",
                            by=XPATH,
                        )
                        ss = self.driver.find_element_by_xpath(
                            "/html/body/div[1]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span"
                        )
                        posttext = ss.text
                        pp = posttext.split()
                        for word in pp:
                            if (
                                word[0] == "#"
                                and (word not in hashtags)
                                and ("#" not in word[1:])
                            ):
                                hashtags.append(word)

                        break
                    except:
                        print("Error Try Again")
            return hashtags
        except:
            print("some error in hashtag")
            return -1

    def scraperhashtagfromuser(self, targetaccount):

        try:
            hashtags = self.__getuserusedhashtag(targetaccount)
            if hashtags != -1:
                Curdate = datetime.now()
                for x in hashtags:
                    for i in range(0, 5):
                        try:
                            SqlData = [targetaccount, x, Curdate]
                            Sqlquery = "INSERT INTO HashtagAccount (Account,Hashtag,Date) Values (%s,%s,%s)"
                            self.mycursor.execute(Sqlquery, SqlData)
                            self.mydb.commit()
                            break
                        except:
                            time.sleep(1)
                            self.__init_db()
                            time.sleep(1)
                return "Success"
        except:
            print("Big error in hashtag")
            return -1

    # if 2 is returned means hashtag scraping is finished
    # Returns Success if done completly
    def gethashtagAccountquality(self):
        try:
            Failed = True
            count = 0
            for i in range(0, 5):
                try:
                    Sqlquery = "SELECT Hashtag FROM HashtagAccount WHERE numpost IS NULL order by Rand() Limit 1"
                    self.mycursor.execute(Sqlquery)
                    for db in self.mycursor:
                        count += 1
                    if count == 0:
                        return 2
                    Failed = False
                    break
                except:
                    time.sleep(1)
                    self.__init_db()
                    time.sleep(1)
            if Failed == False:
                hashtag = db[0]
                url = "https://www.instagram.com/explore/tags/" + hashtag[1:]
                self.driver.get(url)
                time.sleep(5)
                ss = waiter.find_element(
                    self.driver,
                    "/html/body/div[1]/section/main/header/div[2]/div[1]/div[2]/span/span",
                    by=XPATH,
                )
                num = ss.text
                num = num.replace(",", "", 20)
                num = int(num)
                for i in range(0, 5):
                    try:
                        Sqldata = [num, hashtag]
                        Sqlquery = (
                            "Update HashtagAccount SET numpost = %s WHERE Hashtag = %s"
                        )
                        self.mycursor.execute(Sqlquery, Sqldata)
                        self.mydb.commit()
                        return "Success"
                    except:
                        time.sleep(1)
                        self.__init_db()
                        time.sleep(1)
            else:
                print("Error in Hashtag Scraping")
                return -1
        except:
            print("Error in Hashtag Scraping")
            return -1

    def __getuserfollowersscript(self, targetaccount):
        # The link we must go to
        linkprofile = "https://www.instagram.com/" + targetaccount
        self.driver.get(linkprofile)
        time.sleep(round(random.uniform(4, 6), 2))
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        ).click()
        time.sleep(round(random.uniform(4, 6), 2))
        waiter.find_element(self.driver, "//div[@role='dialog']", by=XPATH)
        follower_css = "ul div li:nth-child({}) a.notranslate"
        for group in itertools.count(start=1, step=12):
            # A sleep is necessary so that instagram doesen't block us, FollowDelay is give to the constructor
            # time.sleep(round(random.uniform(self.FollowerDelay-1, self.FollowerDelay+1), 2))
            for follower_index in range(group, group + 12):
                try:
                    current_follower = waiter.find_element(
                        self.driver, follower_css.format(follower_index)
                    )
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", current_follower
                    )
                    time.sleep(0.1)
                    yield waiter.find_element(
                        self.driver, follower_css.format(follower_index)
                    ).text
                except:
                    print("Oh no")
                    return -1
                    # last_follower1 = waiter.find_element(self.driver, follower_css.format(follower_index - 8))
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", last_follower1)
                    # yield waiter.find_element(self.driver, follower_css.format(follower_index)).text
            last_follower = waiter.find_element(
                self.driver, follower_css.format(follower_index)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", last_follower
            )
            time.sleep(0.5)

    def __getuserfollowers(self, targetaccount, printornot=False, max=3000):
        targetaccount = targetaccount.lower()
        try:
            followerCaught = 0
            followertoscrape = 0
            userdata = self.getuserdetails(targetaccount)
            if userdata == -1 or userdata == "UserNotFound":
                print("Error: Couldn't Get user Data")
                return -1
            if userdata[1] == True:
                print("Error: Get UserFollowers, Account is private")
                return -1
            followertoscrape = userdata[4]
            followertoscrape = int(followertoscrape * 0.95)
            if followertoscrape > max:
                followertoscrape = max
            followerslist = []
            for count, follower in enumerate(
                self.__getuserfollowersscript(targetaccount), 1
            ):
                if printornot is True:
                    print(count, ":", follower)
                followerCaught += 1
                followerslist.append(follower)
                if count >= followertoscrape:
                    break

            return followerslist
        except Exception as err:
            print("Error: in UserFollowers")
            traceback.print_exc()
            print(str(err))
            if followertoscrape != 0 and followerCaught / followertoscrape > 0.75:
                print("Got more than 75% so it's fine")
                return followerslist
            return -1

    def scraperfollowers(self, targetaccount, nosql=False):
        try:
            Followerslist = self.__getuserfollowers(targetaccount)
            if nosql is True:
                return Followerslist
            if Followerslist != -1:
                Curdate = datetime.now()
                for x in Followerslist:
                    for i in range(0, 5):
                        try:
                            SqlData = [targetaccount, x, Curdate]
                            Sqlquery = "INSERT INTO Follower (Followed,Follower,DateUpdate) Values (%s,%s,%s)"
                            self.mycursor.execute(Sqlquery, SqlData)
                            self.mydb.commit()
                            break
                        except:
                            time.sleep(1)
                            self.__init_db()
                            time.sleep(1)
                return "Success"
        except:
            print("Big error in scraperfollower")
            return -1

    def __getuserfollowingcript(self, targetaccount):
        # The link we must go to
        linkprofile = "https://www.instagram.com/" + targetaccount
        self.driver.get(linkprofile)
        time.sleep(round(random.uniform(4, 6), 2))
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
        ).click()
        time.sleep(round(random.uniform(4, 6), 2))
        waiter.find_element(self.driver, "//div[@role='dialog']", by=XPATH)
        following_css = "ul div li:nth-child({}) a.notranslate"
        for group in itertools.count(start=1, step=12):
            # A sleep is necessary so that instagram doesen't block us, FollowDelay is give to the constructor
            # time.sleep(round(random.uniform(self.FollowerDelay-1, self.FollowerDelay+1), 2))
            for following_index in range(group, group + 12):
                try:
                    current_following = waiter.find_element(
                        self.driver, following_css.format(following_index)
                    )
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", current_following
                    )
                    time.sleep(0.1)
                    yield waiter.find_element(
                        self.driver, following_css.format(following_index)
                    ).text
                except:
                    return -1
            last_following = waiter.find_element(
                self.driver, following_css.format(following_index)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", last_following
            )
            time.sleep(0.5)

    def __getuserfollowing(self, targetaccount, printornot=False, max=1000):
        targetaccount = targetaccount.lower()
        try:
            followingCaught = 0
            followingtoscrape = 0
            userdata = self.getuserdetails(targetaccount)
            if userdata == -1 or userdata == "UserNotFound":
                print("Error: Couldn't Get user Data")
                return -1
            if userdata[1] == True:
                print("Error: Get Userfollowing, Account is private")
                return -1
            followingtoscrape = userdata[5]
            if followingtoscrape > max:
                followingtoscrape = max
            followinglist = []
            for count, following in enumerate(
                self.__getuserfollowingcript(targetaccount), 1
            ):
                if printornot is True:
                    print(count, ":", following)
                followingCaught += 1
                followinglist.append(following)
                if count >= followingtoscrape:
                    break
            if len(followinglist) >= 0.98 * followingtoscrape:
                return followinglist
            else:
                print("Something Failed")
                return -1

        except Exception as err:
            print("Error: in Userfollowing")
            traceback.print_exc()
            print(str(err))
            return -1

    def scraperfollowing(self, targetaccount, nosql=False):
        try:
            Followerslist = self.__getuserfollowing(targetaccount)
            if nosql is True:
                return Followerslist
            if Followerslist != -1:
                Curdate = datetime.now()
                for x in Followerslist:

                    for i in range(0, 5):
                        try:
                            SqlData = [targetaccount, x, Curdate]
                            Sqlquery = "INSERT INTO Following (Follower,Followed,DateUpdate) Values (%s,%s,%s)"
                            self.mycursor.execute(Sqlquery, SqlData)
                            self.mydb.commit()
                            break
                        except:
                            time.sleep(1)
                            self.__init_db()
                            time.sleep(1)
                return "Success"
        except:
            print("Big error in scraperfollower")
            return -1

    def __del__(self):
        self.driver.close()

    def manager(self, hostaccount):
        try:
            Failed = True
            count = 0
            for i in range(0, 5):
                try:
                    Sqlquery = "SELECT Account FROM SpecialAccount WHERE MainAccount=%s and LikeScraped=False order by Type Limit 1"
                    self.mycursor.execute(Sqlquery, (hostaccount,))
                    for db in self.mycursor:
                        count += 1
                    if count == 0:
                        return 2
                    Failed = False
                    break
                except:
                    time.sleep(1)
                    self.__init_db()
                    time.sleep(1)
            if Failed is True:
                return -1
            usertogetlike = db[0]
            result = self.scraperlikes(usertogetlike, 6)
            if result == "Success":
                for i in range(0, 5):
                    try:
                        SqlData = [self.username, usertogetlike]
                        Sqlquery = "UPDATE SpecialAccount SET LikeScraped=True WHERE MainAccount=%s and Account=%s"
                        self.mycursor.execute(Sqlquery, SqlData)
                        self.mydb.commit()
                        break
                    except:
                        time.sleep(1)
                        self.__init_db()
                        time.sleep(1)
                time.sleep(120)
                return "Success"
            else:
                return -1

        except:
            pass


# PS=PremiumDataScraping('shiva_sami', 'ilove600million*', True, True)
# PS.manager()
# PS.manager()
