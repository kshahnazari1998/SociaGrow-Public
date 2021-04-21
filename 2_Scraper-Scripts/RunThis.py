import subprocess
import time
from VpnConnect import VpnConnects

vpc = VpnConnects()

while True:

    time.sleep(10)

    processf2 = subprocess.Popen(["python", "Targetaccountstatus.py"])
    time.sleep(3600)

    processf2.kill()

    # Scrape User

    processmain = subprocess.Popen(["python", "ManagerAdmin.py"])

    time.sleep(45)
    print("Opened The SubProcesses")

    process1 = subprocess.Popen(["python", "Manager1.py"])
    process2 = subprocess.Popen(["python", "Manager2.py"])
    process3 = subprocess.Popen(["python", "Manager3.py"])
    process4 = subprocess.Popen(["python", "Manager4.py"])
    process5 = subprocess.Popen(["python", "Manager5.py"])

    time.sleep(6000)
    processmain.kill()
    process1.kill()
    process2.kill()
    process3.kill()
    process4.kill()
    process5.kill()

    print("Killed the Managers")
    time.sleep(10)

    subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
    time.sleep(45)
