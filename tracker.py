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
trackedign_low = trackedign.lower()
print(f"Tracking {trackedign}...")



try:
    ruuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{trackedign}")
    udata = ruuid.json()
    uuid = udata["id"]
    rduuid = requests.get(f"{url}/convert?name={trackedign}", headers = headers)
    dudata = rduuid.json()
    dasheduuid = dudata[f'{trackedign_low}']
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


getstats = requests.get(f"https://api.hypixel.net/player?uuid={uuid}", headers = headershyp)
stats = getstats.json()
getwse = requests.post(f"{url}/winstreak", headers = headers, json =  {'igns': [f'{trackedign}']})
wse = getwse.json()


if "Bedwars" in stats["player"]["stats"] and "winstreak" in stats["player"]["stats"]["Bedwars"]:
    bwCWS = stats["player"]["stats"]["Bedwars"]["winstreak"]
else:
    bwCWS = "N/A"

if "Duels" in stats["player"]["stats"] and "current_winstreak" in stats["player"]["stats"]["Duels"]:
    duelsCWS = stats["player"]["stats"]["Duels"]["current_winstreak"]
else:
    duelsCWS = "N/A"

if dasheduuid in wse["data"]["uuids"]:
    bwWSE = wse["data"]["uuids"][dasheduuid]["data"]["overall_winstreak"]
else:
    bwWSE = "N/A"


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

        time.sleep(2)
        r2 = requests.get(f"{urlhyp}/status?uuid={uuid}", headers = headershyp)
        data2 = r2.json()
        ses2 = data2["session"]

        ses = diff(ses1, ses2)

        if bool(ses):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
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

        time.sleep(4)
        r2 = requests.get(f"{urlhyp}/recentgames?uuid={uuid}", headers = headershyp)
        data2 = r2.json()
        gamelast2 = data2["games"][0]

        gamelast = diff(gamelast1, gamelast2)

        if bool(gamelast):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            gametype = gamelast2["gameType"]
            map = gamelast2["map"]
            mode = gamelast2["mode"]
            if "ended" in gamelast2:
                print("")
                print(f"[{current_time}] >> Hypixel API || {trackedign}'s recent games updated:")
                print(f"-- Finished a game of {gametype}")
                print(f"-- mode: {mode}")
                print(f"-- map: {map}")               
            else:
                print("")
                print(f"[{current_time}] >> Hypixel API || {trackedign}'s recent games updated:")
                print(f"-- Started a game of {gametype}")
                print(f"-- mode: {mode}")
                print(f"-- map: {map}")
            gamelast = {}
            time.sleep(3)


#===========
#ANTISNIPER
#===========

antisniper = False

if statusapi == False:
    print("")
    print(">> Trying to use Antisniper API...")
    player = requests.get(f"{url}/player/v2?uuid={dasheduuid}", headers = headers)
    playerdata = player.json()
    if playerdata["success"] == True:
        if playerdata["player"]["times_seen"] > 0:
            print(">> SUCCESS! Using Antisniper API bot queue tracking method...")
            antisniper = True
        else:
            print(">> Tracked player not in database.")
            antisniper = False
    else:
        pprint(playerdata["cause"])

def useantisniperLEGACY():
    while antisniper == True:
        r = requests.get(f"{url}/botqueues", headers = headers)
        data = r.json()

        r2 = requests.get(f"{url}/botstatus", headers = headers)
        data2 = r2.json()

        botlist = []
        #botstatus = None

        for botname in data["data"]:
            botlist.append(botname)


        for getbotname in botlist:
            if trackedign in data["data"][getbotname]["queue"]:
                #if botstatus != data2["data"][getbotname]:
                    print("")
                    print(f">> Antisniper API || {trackedign} is in {getbotname}'s queue")
                    botstatus = data2["data"][getbotname]
                    print(f"-- server: {botstatus['server']}")
                    print(f"-- mode: {botstatus['mode']}")
                    print(f"-- map: {botstatus['map']}")
            #else:
                #botstatus = None
    
        time.sleep(3)

def useantisniper():
    while antisniper == True:
        botr = requests.get(f"{url}/botlist", headers = headers)
        botdata = botr.json()
        botlist = botdata["botlist"]

        r2 = requests.get(f"{url}/botqueues/v3", headers = headers)
        data2 = r2.json()

        time.sleep(2)

        r = requests.get(f"{url}/botqueues/v3", headers = headers)
        data = r.json()

        for bot in botlist:
            if data2["data"][bot]["server"] != data["data"][bot]["server"]:
                for ignlists in data["data"][bot]["last_queue"]:
                    if trackedign_low == ignlists["ign_lower"]:
                        server = data["data"][bot]["server"]
                        map = data["data"][bot]["map"]
                        mode = data["data"][bot]["mode"]
                        print("")
                        print(f">> Antisniper API || {trackedign} is in {bot}'s queue")
                        print(f"-- server: {server}")
                        print(f"-- mode: {mode}")
                        print(f"-- map: {map}")


thread = threading.Thread(target=usestatusapi)
thread.start()

thread = threading.Thread(target=userecentapi)
thread.start()

thread = threading.Thread(target=useantisniper)
thread.start()