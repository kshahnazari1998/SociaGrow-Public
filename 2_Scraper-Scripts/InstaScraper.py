import itertools
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from explicit import waiter, XPATH
import time
import random
import pickle
import re
import sys
import requests
import traceback


class InstaScraper:

    # The constructor
    # FollowerDelay is the time which is spent between each scroll of follower scraping
    # Show or not is for making the browser headless or not (Meaning show on execute)

    def __init__(
        self,
        driverpath,
        username="",
        password="",
        cookiepath="",
        FollowerDelay=6,
        showornot=False,
    ):
        try:
            self.driverpath = driverpath
            self.username = username
            self.password = password
            self.cookiepath = cookiepath
            self.showornot = showornot
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            if self.showornot == False:
                self.driver = webdriver.Chrome(
                    executable_path="chromedriver.exe", options=options
                )
            else:
                self.driver = webdriver.Chrome(self.driverpath)
            self.driver.get("https://www.google.com")
            self.FollowerDelay = FollowerDelay
            self.loggedin = False
            time.sleep(2)
        except Exception as e:
            print(e)

    def resetbrowser(self):
        self.driver.quit()
        time.sleep(5)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        if self.showornot == False:
            self.driver = webdriver.Chrome(
                executable_path="chromedriver.exe", options=options
            )
        else:
            self.driver = webdriver.Chrome(self.driverpath)
        self.driver.get("https://www.google.com")
        self.loggedin = False
        time.sleep(2)

    """
    # So This was written but didn't work because proxies were to slow
    # If one day we have enough proxies we can use them.
    def changeproxy(self):
        #I got some free proxies for this site and opened up the response json for the ip
        response=requests.get("https://gimmeproxy.com/api/getProxy")
        response=response.json()
        ip=response['ip']
        port=response['port']
        myip=ip + ":" + port
        print(myip)
        #open up the chrome with the ip
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % myip)
        self.driver.quit()
        time.sleep(1)
        self.driver = webdriver.Chrome(self.driverpath,options=chrome_options)
        self.driver.get("https://www.google.com")
    """

    def Login(self):
        # Check that if we already logged in there is no need to do it again
        if self.loggedin is True:
            print("Already Logged in")
            return 1
        try:
            # Open driver and load cookies
            self.driver.get("https://www.instagram.com/accounts/login")
            cookies = pickle.load(open(self.cookiepath, "rb"))
            for cookie in cookies:
                if "expiry" in cookie:
                    del cookie["expiry"]
                self.driver.add_cookie(cookie)
            time.sleep(round(random.uniform(5, 7), 2))
            # Check if we are not already logged in on last session
            cururl = self.driver.current_url
            if cururl == "https://www.instagram.com/":
                print("Already Logged In no need To Login")
                return -1
            # Everything is fine we are logged in Let's fill the form
            waiter.find_write(self.driver, "//input", self.username, by=XPATH)
            time.sleep(round(random.uniform(2, 3), 2))
            waiter.find_write(
                self.driver, "//div[3]/div/label/input", self.password, by=XPATH
            )
            time.sleep(round(random.uniform(2, 3), 2))
            waiter.find_element(self.driver, "//button/div", by=XPATH).click()
            time.sleep(round(random.uniform(4, 6), 2))
            # Check if login was successful
            cururl = self.driver.current_url
            if cururl == "https://www.instagram.com/":
                print("Login success")
                pickle.dump(self.driver.get_cookies(), open(self.cookiepath, "wb"))
                self.loggedin = True
                return 0
            # We didn't get to the main page so there was a problem
            else:
                print("Error: Login Was not successful")
                return -1
        except Exception as err:
            print("Error: in Login")
            traceback.print_exc()
            print(str(err))
            return -1

    def get_disconnected_msg(self):
        return "Unable to evaluate script: disconnected: not connected to DevTools\n"

    # Function to remove Emoji from Text because emojis can't be saved in Sql Database
    # I don't know how it works but it does the job :D
    def __strip_emoji(self, text):
        RE_EMOJI = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
        return RE_EMOJI.sub(r"", text)

    # Gets basic information like bio, posts , followers , following , privatepublic and verified
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
                if (
                    "old or over to"
                    in self.driver.find_element_by_xpath(
                        "/html/body/div/div[1]/div/div"
                    ).text.strip()
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
            if "https://www.instagram.com/accounts/login/" in url:
                return -10

            # for other errors this is it.
            if "list" in str(err):
                traceback.print_exc()
                print("Stop")
            traceback.print_exc()
            print(str(err))
            return -1

    # We don't call this function from outside. for the use of getuserfollowers
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

    def getuserfollowers(self, targetaccount, printornot=False):
        # if not logged in we need to login first
        if self.loggedin is False:
            success = self.Login()
            if success == -1:
                return -1

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
            followertoscrape = int(followertoscrape * 0.9)
            if followertoscrape > 2000:
                followertoscrape = 2000
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
            if followertoscrape != 0 and followerCaught / followertoscrape > 0.85:
                print("Got more than 85% so it's fine")
                return followerslist
            return -1

    # FOLLOWING
    # We don't call this function from outside. for the use of getuserfollowing
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

    def getuserfollowing(self, targetaccount, printornot=False):
        # if not logged in we need to login first
        if self.loggedin is False:
            success = self.Login()
            if success == -1:
                return -1

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
