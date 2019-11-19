import json
import time
import datetime
import pandas as pd
import numpy

WEEK_IN_SECONDS = 604800
CURRENT_UNIX_TIME = datetime.datetime.now().timestamp()

def getUniversityIDs(json_file_name):
    uniIDDict = {}
    with open(json_file_name, errors = "ignore") as json_file:
        wabuJSON = json.load(json_file)
    
    for i in wabuJSON["UNIVERSITY"].keys():
        uniIDDict[i] = wabuJSON["UNIVERSITY"][i]["FULLNAME"]
        print(wabuJSON["UNIVERSITY"][i]["FULLNAME"])
    
    return uniIDDict
    
def getUniDomains(json_file_name):
    uniDomainDict = {}
    with open(json_file_name, errors = "ignore") as json_file:
        wabuJSON = json.load(json_file)
    
    for i in wabuJSON["UNIVERSITY"].keys():
        uniDomainDict[wabuJSON["UNIVERSITY"][i]["EMAILDOMAIN"]] = i 
        print(wabuJSON["UNIVERSITY"][i]["FULLNAME"])
    
    return uniDomainDict

def getWeeklyUsers(json_file_name):
    uniIDDict = getUniversityIDs(json_file_name)
    uniDomainDict = getUniDomains(json_file_name)
    userList = []
    uniIDList = []
    indexList = []
    userMatrix = [[]]
    emailList = []
    dateList = []
    wabuJSON = None

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
            dateList.append(date)
            try:
                if ("UNIVERSITY_ID" in userJSON[i].keys()):
                    uniIDList.append(uniIDDict[userJSON[i]["UNIVERSITY_ID"]])
                else:
                    uniIDDict[uniDomainDict[userJSON[i]["EMAIL"].split("@")[1]]]
                    uniIDList.append(uniIDDict[uniDomainDict[userJSON[i]["EMAIL"].split("@")[1]]])

                    #uniIDList.append("UNIVERSITY_ID_NOT_FOUND")
            except:
                uniIDList.append(userJSON[i]["UNIVERSITY_ID"])
    
    dataDict = {"email": emailList, "date_of_use": dateList, "geofence": uniIDList}
    df = pd.DataFrame(data=dataDict, index = indexList)
    df = df.sort_values("date_of_use")
    df.to_csv('weeklyUsers.csv')
    return df

def getWeeklyUsersByGeofence(df, geofence):
    newDF = df[df["geofence"] == geofence]
    newDF.to_csv('weeklyUsers' + geofence + ".csv")
    return newDF

json_file_name = input("Input JSON file name: ")
print("Here are the different geofences: ")

geofence_name = input("Input which domain you want to find, enter \nno if you don't want to separate by geofence: ")

weeklyUserDF = getWeeklyUsers(json_file_name)
if (geofence_name != "no"):
    getWeeklyUsersByGeofence(weeklyUserDF, geofence_name)



