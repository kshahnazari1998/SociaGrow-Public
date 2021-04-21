import itertools
from selenium import webdriver
from explicit import waiter, XPATH
import time
import random
import pickle
import re
import requests
import traceback

print("Write the name of the cookie")
cookiename = input()

print("Login into instagram and then write Done in console")

driver=webdriver.Chrome("chromedriver.exe")

while True:
    inp = input()
    if inp.strip().lower() == 'done':
        pickle.dump(driver.get_cookies(), open(cookiename + ".txt", "wb"))
        break