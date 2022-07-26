from aiohttp import request
import json
import requests
import asyncio
from pprint import pprint
import time
from os import path
import jsondiff as jd
from jsondiff import diff
from colorama import Fore, Back, Style
import threading
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

url = "https://api.antisniper.net"
urlhyp = "https://api.hypixel.net"

#load settings
file = open('settings.json', 'r', encoding='unicode_escape')
json_object = json.load(file)
file.close()
keya = json_object["antisniper-api-key"]
keyh = json_object["hypixel-api-key"]



headers = {
    "Apikey": f"{keya}",
    "Content-Type": "application/json"}
headershyp = {
    "API-KEY": f"{keyh}",
    "Content-Type": "application/json"}

print("===========================================")
print("  CRYME TRACKER ALPHA UNSTABLE RELEASE 1")
print("===========================================")
print("       > made by azurim#8202 <")
print("")
trackedign = input("Enter ign: ")
print(f"Tracking {trackedign}...")



try:
    ruuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{trackedign}")
    udata = ruuid.json()
    uuid = udata["id"]
    rduuid = requests.get(f"{url}/convert?name={trackedign}", headers = headers)
    dudata = rduuid.json()
    dasheduuid = dudata[f'{trackedign}']
except Exception as e:
    print("")
    print("=================================================================")
    print("ERROR OCCURED, MAKE SURE THAT YOU ARE ENTERING AN EXISTING PLAYER")
    print("=================================================================")
    print("")
    print("Exception:")
    print(e)
    print("")
    print("=================================================================")
    print("           TO CONTINUE, PLEASE REOPEN THE PROGRAM")
    print("=================================================================")
    print("")

#print(uuid)

getstats = requests.get(f"https://api.hypixel.net/player?uuid={uuid}", headers = headershyp)
stats = getstats.json()
getwse = requests.post(f"{url}/winstreak", headers = headers, json =  {'igns': [f'{trackedign}']})
wse = getwse.json()

if "winstreak" in stats["player"]["stats"]["Bedwars"]:
    bwCWS = stats["player"]["stats"]["Bedwars"]
else:
    bwCWS = "N/A"

if "current_winstreak" in stats["player"]["stats"]["Duels"]:
    duelsCWS = stats["player"]["stats"]["Duels"]["current_winstreak"]
else:
    duelsCWS = "N/A"

bwWSE = wse["data"]["uuids"][dasheduuid]["data"]["overall_winstreak"]

print("")
print(f">> Hypixel API || Bedwars CWS: {bwCWS}, Duels CWS: {duelsCWS}")
print(f">> Antisniper API || Estimated Bedwars WS: {bwWSE}")



r = requests.get(f"{urlhyp}/status?uuid={uuid}", headers = headershyp)
data = r.json()
print("")
print(">> Trying to use Hypixel API status endpoint...")

#=============
#ONLINE STATUS
#=============

if data["session"]["online"] is not False: 
    #pprint(data["session"])
    print("SUCCESS! >> Using online status method...")
    statusapi = True
        
else:
    print(f">> {trackedign} is offline or has their status api disabled")
    statusapi = False

def usestatusapi():
    while statusapi == True:
        r1 = requests.get(f"{urlhyp}/status?uuid={uuid}", headers = headershyp)
        data1 = r1.json()
        ses1 = data1["session"]
        #print(f"ses1: {ses1}")

        time.sleep(3)
        r2 = requests.get(f"{urlhyp}/status?uuid={uuid}", headers = headershyp)
        data2 = r2.json()
        ses2 = data2["session"]
        #print(f"ses2: {ses2}")

        ses = diff(ses1, ses2)
        #print(f"ses (dif): {ses}")

        if bool(ses):
            #print(f"ses1 (update): {ses2}")
            print("")
            print(f"[{current_time}] >> Hypixel API || {trackedign}'s status updated:")
            if "gameType" in ses2:
                gametype = ses2["gameType"]
                print(f"-- gameType: {gametype}")
            if "mode" in ses2:
                mode = ses2["mode"]
                print(f"-- mode: {mode}")
            if "map" in ses2:
                map = ses2["map"]
                print(f"-- map: {map}")
            ses = {}


#============
#RECENT GAMES
#============

getrece = requests.get(f"{urlhyp}/recentgames?uuid={uuid}", headers = headershyp)
recent = getrece.json()
print("")
print(">> Trying to use Hypixel API recent games endpoint...")
games = recent["games"]
if len(games):
    print("SUCCESS! >> Using Hypixel API recent games method...")
    recentapi = True
else:
    print(f">> {trackedign} has their recent games API disabled")
    recentapi = False

def userecentapi():
    while recentapi == True:
        r1 = requests.get(f"{urlhyp}/recentgames?uuid={uuid}", headers = headershyp)
        data1 = r1.json()
        gamelast1 = data1["games"][0]
        #pprint(f"gamelast1: {gamelast1}")

        time.sleep(5)
        r2 = requests.get(f"{urlhyp}/recentgames?uuid={uuid}", headers = headershyp)
        data2 = r2.json()
        gamelast2 = data2["games"][0]
        #pprint(f"gamelast2: {gamelast2}")

        gamelast = diff(gamelast1, gamelast2)

        if bool(gamelast):
            gametype = gamelast2["gameType"]
            map = gamelast2["map"]
            mode = gamelast2["mode"]
            if "ended" in gamelast2:
                print("")
                print(f"[{current_time}] >> Hypixel API || {trackedign}'s recent games updated:")
                print(f"-- Finished a game of {gametype}")
                print(f"-- map: {map}")
                print(f"-- mode: {mode}")
            else:
                print("")
                print(f"[{current_time}] >> Hypixel API || {trackedign}'s recent games updated:")
                print(f"-- Started a game of {gametype}")
                print(f"-- map: {map}")
                print(f"-- mode: {mode}")
            gamelast = {}
            time.sleep(5)


#===========
#ANTISNIPER
#===========

if statusapi == False:
    print("Antisniper API mode enabled")


thread1 = threading.Thread(target=usestatusapi)
thread1.start()

thread1 = threading.Thread(target=userecentapi)
thread1.start()