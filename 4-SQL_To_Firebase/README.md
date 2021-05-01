In this step, we need to create a scraper that actively scrapes the finished Dota 2 games and adds them to the MySQL database we created in the step before. The instructions are written below in order.

1) Get your Firebasecredentials.json from google and replace the file here with it.
3) Create a Computer Engine (Seperate from the one we created from step 2 because that computer engine would be IP swapping and must be separate from this engine. with the minimum computational power and Ubuntu operating system. Install Python 3.8.8 on that Engine and make sure the pip command works in the terminal.
3) To handle the dependencies of the scripts, two approaches could be taken. Either pip installing the libraries or using conda. Using pip install is faster because not many dependencies to handle, and install conda would take a lot of unnecessary time. The list below shows the required packages. Run these lines one by one.
```
pip install pandas==1.2.2
pip install pymysql==1.0.2
pip install mysql-connector-python==8.0.23
pip install firebase-admin
```
4) Upload the files in this folder to the computer engine.
5) We want the script to train and upload the new models every hour. Todo, so we need crontab to do this.

```
#10 * * * * cd FOLDERWITHSCRIPT && python TargetAccountdatabase.py
#15 * * * * cd FOLDERWITHSCRIPT && python TargetAccountdatabaseerrors.py
#20 * * * * cd FOLDERWITHSCRIPT && python TaskBank.py
#25 1 * * * cd FOLDERWITHSCRIPT && python TaskGiverFirebaseSQL.py
#30 1 * * * cd FOLDERWITHSCRIPT && python TaskGiverSQL.py
#35 1 * * * cd FOLDERWITHSCRIPT && python TaskIncrease.py
#40 * * * * cd FOLDERWITHSCRIPT && python UserData.py
```
