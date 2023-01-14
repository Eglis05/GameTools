import requests
from bs4 import BeautifulSoup
import time
import os
import sys
from urllib.request import urlopen
from datetime import datetime

clan_id = 4064 #RUH: 5555, BB: 102, ZE: 4064, LPC: 8029, OOC: 6119
one_interval = 60
values = [1000, 1, 5, 10, 30]
names = ["total gain", "last 1 min"]
names.extend([f"last {x} mins" for x in values[2:]])

def get_td_values(link):
    webp = requests.get(link).text
    soup = BeautifulSoup(webp, "html.parser")
    return soup.find_all("td")

def get_reps():
    links = [f"https://technotal.com/shinobi_warfare/clan-members.php?clan_id={clan_id}", f"https://technotal.com/shinobi_warfare/clan-members.php?clan_id={clan_id}&page=1", f"https://technotal.com/shinobi_warfare/clan-members.php?clan_id={clan_id}&page=2"]
    td_values = []
    for link in links:
        td_values.extend(get_td_values(link))
    players = {}
    for i in range(0, len(td_values), 3):
        name = td_values[i].text
        while name in players.keys():
            name = name + " Jr."

        rep = td_values[i + 2].text
        players[name] = int(rep)
    return players

def table(initial_rep, total_rep, changes):
    sorted_names = list(dict(sorted(changes[names[2]].items(), key=lambda item: item[1], reverse=True)).keys())
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')
    print('|{0:3s} | {1:20s} | {2:10s} | {3:8s} | {4:9s} | {5:6s} | {6:6s} | {7:7s} | {8:7s}'.format("Pos", "Char Name", "initialRep", "totalRep", "totalGain", f"last {values[1]}", f"last {values[2]}", f"last {values[3]}", f"last {values[4]}"), flush=True)
    line = "-" * 102
    print(line , sep="", end = "\n", flush=True)
    print('|{0:3d} | {1:20s} | {2:10d} | {3:8d} | {4:9d} | {5:6d} | {6:6d} | {7:7d} | {8:7d}'.format(0, f"Clan {clan_id}", sum(initial_rep.values()), sum(total_rep.values()), sum(changes["total gain"].values()), sum(changes[f"last {values[1]} min"].values()), sum(changes[f"last {values[2]} mins"].values()), sum(changes[f"last {values[3]} mins"].values()), sum(changes[f"last {values[4]} mins"].values())), flush=True)
    print(line , sep="", end = "\n", flush=True)
    for i in range(len(sorted_names)):
        char_name = sorted_names[i]
        print('|{0:3s} | {1:20s} | {2:10d} | {3:8d} | {4:9d} | {5:6d} | {6:6d} | {7:7d} | {8:7d}'.format(f"{i+1}", char_name, initial_rep[char_name], total_rep[char_name], changes["total gain"][char_name], changes[f"last {values[1]} min"][char_name], changes[f"last {values[2]} mins"][char_name], changes[f"last {values[3]} mins"][char_name], changes[f"last {values[4]} mins"][char_name]), flush=True)
    sys.stdout.flush()

def update_burnlist(burnlist, old_burnlist, burntime, changes):
    change = {}
    for item in burnlist:
        if item not in old_burnlist.keys():
            old_burnlist[item] = 0
            for i in values:
                burntime[i][item] = 0
            for i in names:
                changes[i][item] = 0
        change[item] = burnlist[item] - old_burnlist[item]
    for item in old_burnlist:
        if item not in burnlist.keys():
            for i in values:
                burntime[i].pop(item)
            for i in names:
                changes[i].pop(item)
    return change, burntime, changes

def check_validity():
    res = urlopen('http://just-the-time.appspot.com/')
    result = res.read().strip().decode('utf-8')
    today_date = datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
    if today_date >= datetime.strptime("2023-01-20", '%Y-%m-%d'):
        return False
    else:
        return True

if __name__ == "__main__":
    if check_validity():
        start = time.time()
        start_players = get_reps()
        old_burntime = {}
        for i in values:
            old_burntime[i] = start_players.copy()
        change = {}
        for name in names:
            change[name] = {k: 0 for k in old_burntime[values[0]]}
        counter = 0
        while True:
            time.sleep(max(one_interval - (time.time() - start), 0))
            start = time.time()
            counter += 1
            try:
                burnlist = get_reps()
            except:
                burnlist = old_burntime[values[1]]
            for i in range(len(values)):
                if counter % values[i] == 0 or i == 0:
                    change_i, old_burntime, change = update_burnlist(burnlist, old_burntime[values[i]], old_burntime, change)
                    change[names[i]] = change_i
                    if i != 0:
                        old_burntime[values[i]] = burnlist
            table(old_burntime[values[0]], burnlist, change)    
