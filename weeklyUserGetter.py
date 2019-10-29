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
dayList = []
wabuJSON = None

with open('WaBu Data.json', errors = "ignore") as json_file:
    wabuJSON = json.load(json_file)
    
for i in wabuJSON["USERS"].keys():
    userList.append(i)

userList.remove("GROUPS")
userList.remove("USER_GROUPS")
userList = userList[1:]

userJSON = wabuJSON["USERS"]
for i in userList:

    secondsElapsed = CURRENT_UNIX_TIME - wabuJSON["USERS"][i]["TIME_MILLIS"]
    if (secondsElapsed <= WEEK_IN_SECONDS):
        indexList.append(userJSON[i]["USER_NAME"])
        emailList.append(userJSON[i]["EMAIL"])
        daysSinceUse = secondsElapsed / 60 / 60 / 24
        dayList.append(daysSinceUse)
        


dataDict = {"email": emailList, "days_since_use": dayList}
df = pd.DataFrame(data=dataDict, index = indexList)
df.to_csv('users.csv')
# 1572255490.7196
