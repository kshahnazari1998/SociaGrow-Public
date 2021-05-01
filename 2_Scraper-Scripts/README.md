In this step, we need to create a scraper that actively scrapes related business and public instagram accounts and adds them to the MySQL database we created in the step before. The instructions are written below in order.

1) Add the login information for the database we created before to the scripts Manager1 to Manager5 and ManagerFollower1 on line 30. 
2) Create a Computer Engine (We tested on Google Cloud) with the minimum computational power and Ubuntu operating system. Install Python 3.8.8 on that Engine and make sure the pip command works in the terminal.
3) To handle the dependencies of the scripts, two approaches could be taken. Either pip installing the libraries or using conda. Using pip install is faster because not many dependencies to handle, and install conda would take a lot of unnecessary time. The list below shows the required packages. Run these lines one by one.
```
pip install pandas==1.2.2
pip install pymysql==1.0.2
pip install mysql-connector-python==8.0.23
pip install numpy
pip install selenium
pip install explicit
```
4) Upload the files in this folder to the computer engine.
5) Install screen on the terminal with the code below:
```
apt-get install screen
```
screen needs to be installed on the computer engine so after the terminal is closed, the scripts keep working. create a new session with the command
```
Screen -S Scrapersession
```
6) Run the code `python Runthis.py` and then detach the screen by pressing Ctrl + Alt + D and then close the terminal.
