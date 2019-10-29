import json
import time
import datetime
import pandas as pd
import numpy

WEEK_IN_SECONDS = 604800
CURRENT_UNIX_TIME = datetime.datetime.now().timestamp()
userList = []
indexList = []
userMatrix = [[]]
emailList = []
dateList = []
wabuJSON = None

json_file_name = input("Input JSON File name in same folder as this file: ")
with open(json_file_name, errors = "ignore") as json_file:
    wabuJSON = json.load(json_file)
    
for i in wabuJSON["USERS"].keys():
    userList.append(i)

userList.remove("GROUPS")
userList.remove("USER_GROUPS")
userList = userList[1:]

userJSON = wabuJSON["USERS"]
for i in userList:
    UNIXSeconds = wabuJSON["USERS"][i]["TIME_MILLIS"]
    secondsElapsed = CURRENT_UNIX_TIME - UNIXSeconds
    if (secondsElapsed <= WEEK_IN_SECONDS):
        indexList.append(userJSON[i]["USER_NAME"])
        emailList.append(userJSON[i]["EMAIL"])
        date = str(datetime.datetime.utcfromtimestamp(UNIXSeconds).strftime("%Y-%m-%d %H:%M:%S"))
        print(type(date))
        #daysSinceUse = secondsElapsed / 60 / 60 / 24
        dateList.append(date)
        


dataDict = {"email": emailList, "date_of_use": dateList}
df = pd.DataFrame(data=dataDict, index = indexList)
df = df.sort_values("date_of_use")
df.to_csv('users.csv')
# 1572255490.7196
