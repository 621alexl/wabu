import json
import time
import datetime
import pandas as pd
import numpy
import os

TIME_THRESHOLD = 604800
CURRENT_UNIX_TIME = datetime.datetime.now().timestamp()


json_file_name = input("Input JSON file name: ")


with open(json_file_name, errors = "ignore") as json_file:

        wabuJSON = json.load(json_file)

userToWalkDict = {}
idToNameDict = {}
for i in wabuJSON["USERS"].keys():
    if i == "0":
        continue
    if (i != "GROUPS" and i != "USER_GROUPS"):
        userToWalkDict[i] = 0
    #print(wabuJSON["USERS"][i])
    try:
        idToNameDict[i] = wabuJSON["USERS"][i]["USER_NAME"]
    except:
        #print("error")

        
    

for i in wabuJSON["WALK_REQUESTS"].keys():
    if (CURRENT_UNIX_TIME - wabuJSON["WALK_REQUESTS"][i]["DATE_MILLIS"] <= TIME_THRESHOLD):
        print(idToNameDict[i])
        userToWalkDict[i] = userToWalkDict[i] + 1

walkCounts = []
userNames = []
for i in userToWalkDict.keys():
    userNames.append(idToNameDict[i])
    walkCounts.append(userToWalkDict[i])

df = pd.DataFrame(data = {"has_sent_walk_in_last_week": walkCounts}, index=userNames)
df = df.sort_values("has_sent_walk_in_last_week", ascending=False)
df.to_csv('weeklyWalkRequests.csv')

os.system("start EXCEL.EXE weeklyWalkRequests.csv")