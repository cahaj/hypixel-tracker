import requests
import json
import os
os.system('color')
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()
import time

urlAS = "https://api.antisniper.net"
url = "https://api.hypixel.net"

#load settings
file = open('settings.json', 'r', encoding='unicode_escape')
json_object = json.load(file)
file.close()
keya = json_object["antisniper-api-key"]
keyh = json_object["hypixel-api-key"]

headersAS = {
    "Apikey": f"{keya}",
    "Content-Type": "application/json"}
headers = {
    "API-KEY": f"{keyh}",
    "Content-Type": "application/json"}

def check(uuid: str):
    status = False
    recentgames = False

    r = requests.get(f"{url}/status?uuid={uuid}", headers = headers)
    data = r.json()
    if data["session"]["online"] is not False: 
        status = True     


    getrece = requests.get(f"{url}/recentgames?uuid={uuid}", headers = headers)
    recent = getrece.json()
    games = recent["games"]
    if len(games):
        recentgames = True

    return status, recentgames


def main():
    print(f"{Fore.RED}>> Cryme Tracker by {Fore.LIGHTRED_EX}azurim{Style.RESET_ALL} {Fore.RED}<<{Style.RESET_ALL}")
    print("")
    trackedign = input(f"{Fore.LIGHTRED_EX}Enter ign {Fore.RED}>>{Style.RESET_ALL} ")
    trackedign_low = trackedign.lower()

    try:
        ruuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{trackedign}")
        udata = ruuid.json()
        uuid = udata["id"]
    except Exception as e:
        print(f"{Fore.RED}!!{Style.RESET_ALL} Error occured, make sure you are using a valid ign and api key.")
        print(f"{Fore.RED}Exception >>{Style.RESET_ALL} {e}")

    print(f"{Fore.RED}>>{Style.RESET_ALL} Tracking {uuid}")

    getstats = requests.get(f"https://api.hypixel.net/player?uuid={uuid}", headers = headers)
    stats = getstats.json()

    if "Bedwars" in stats["player"]["stats"] and "winstreak" in stats["player"]["stats"]["Bedwars"]:
        bwCWS = stats["player"]["stats"]["Bedwars"]["winstreak"]
    else:
        bwCWS = "N/A"

    if "Duels" in stats["player"]["stats"] and "current_winstreak" in stats["player"]["stats"]["Duels"]:
        duelsCWS = stats["player"]["stats"]["Duels"]["current_winstreak"]
    else:
        duelsCWS = "N/A"
    
    print(f"""
{Fore.LIGHTRED_EX}Bedwars {Fore.RED}>>{Style.RESET_ALL} {bwCWS}
{Fore.LIGHTRED_EX}Duels {Fore.RED}>>{Style.RESET_ALL} {duelsCWS}""")

    status, recentgames = check(uuid=uuid)
    print(f"{Fore.LIGHTRED_EX}API {Fore.RED}>>{Style.RESET_ALL} status = {status}, recetgames = {recentgames}")

    invalid = True
    valid = ["d", "duels", "bw", "bedwars"]
    if status == True:
        valid.extend(["status", "s"])
    if recentgames == True:
        valid.extend(["recentgames", "recent", "rg"])

    while invalid == True:
        print("")
        track = input(f"{Fore.LIGHTRED_EX}Track {Fore.RED}>>{Style.RESET_ALL} ")
        if track in valid:
            invalid = False
        else:
            print(f"{Fore.RED}!!{Style.RESET_ALL} Invalid input; valid = {Fore.LIGHTWHITE_EX}{valid}{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
    input()