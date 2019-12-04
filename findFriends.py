import json
import time
import datetime
import pandas as pd
import numpy
import os


json_file_name = input("Input JSON file name: ")
with open(json_file_name, errors = "ignore") as json_file:
        wabuJSON = json.load(json_file)


userList = []
friendCountList = []
for i in wabuJSON["USERS"].keys():
    if "USER_NAME" in wabuJSON["USERS"][i].keys():
        userName = wabuJSON["USERS"][i]["USER_NAME"]
        userID = i
        counter = 0

        userList.append(userName)
        if i not in wabuJSON["FRIENDSHIP_REQUESTS"].keys():
            friendCountList.append(0)    
            continue
        for z in wabuJSON["FRIENDSHIP_REQUESTS"][i].keys():
            if wabuJSON["FRIENDSHIP_REQUESTS"][i][z] == "granted":
                counter = counter + 1
        friendCountList.append(counter)

dataDict = {"friend_count": friendCountList}
df = pd.DataFrame(data=dataDict, index = userList)
df = df.sort_values("friend_count", ascending=False)
df.to_csv('friendCounts.csv')

os.system("start EXCEL.EXE friendCounts.csv")