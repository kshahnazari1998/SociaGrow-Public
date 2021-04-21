import pyautogui
import time
import cv2
import numpy as np
import subprocess
import os


# Caution This Vpn Changer is only Written For NORDVPN!!!
class VpnChanger:

    #pause between each action
    def __init__(self,vpnlist):
        self.vpntexts = vpnlist
        self.counter = 0

    
    def changevpn(self):     
        vpnsuc = -1
        for i in range(0,10):
            vpnsuc = self.trychangevpn()
            if vpnsuc==0:
                break
            else:
                self.counter +=1
                if (self.counter==len(self.vpntexts)):
                    break
        if vpnsuc==-1:
            print('Big error in change vpn for some reason')

    def trychangevpn(self):
        try:
            os.popen('"C:/Program Files (x86)/NordVPN/nordvpn" -d')
            time.sleep(10)
            curip = os.popen('nslookup myip.opendns.com resolver1.opendns.com').read()
            pos = curip.find('myip.opendns.com')
            if (pos==-1):
                return -1
            oscommand = '"C:/Program Files (x86)/NordVPN/nordvpn" -c -n ' + '"' +  self.vpntexts[self.counter] + '"'
            os.popen(oscommand)
            time.sleep(45)
            chngip = os.popen('nslookup myip.opendns.com resolver1.opendns.com').read()
            if (chngip.find('myip.opendns.com')!=-1 and chngip!=curip):
                return 0
            else:
                return -1
        except:
            print('Error in trychange vpn')
            return -1




        

