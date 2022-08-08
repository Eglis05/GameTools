import requests
from bs4 import BeautifulSoup
import time
import os

clan_id = 102
one_interval = 60
values = [1000, 1, 5, 10, 30]

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
        while True:
            if name in players.keys():
                name = name + " Jr."
            else:
                break

        rep = td_values[i + 2].text
        players[name] = int(rep)
    return players

def table(initial_rep, total_rep, changes):
    sorted_names = list(dict(sorted(changes["total gain"].items(), key=lambda item: item[1], reverse=True)).keys())
    os.system('clear')
    print('|{0:3s} | {1:20s} | {2:8s} | {3:10s} | {4:9s} | {5:6s} | {6:6s} | {7:7s} | {8:7s}'.format("Pos", "Char Name", "totalRep", "initialRep", "totalGain", f"last {values[1]}", f"last {values[2]}", f"last {values[3]}", f"last {values[4]}"))
    line = "-" * 102
    print(line , sep="", end = "\n")
    print('|{0:3d} | {1:20s} | {2:8d} | {3:10d} | {4:9d} | {5:6d} | {6:6d} | {7:7d} | {8:7d}'.format(0, f"Clan {clan_id}", sum(total_rep.values()), sum(initial_rep.values()), sum(changes["total gain"].values()), sum(changes[f"last {values[1]} min"].values()), sum(changes[f"last {values[2]} mins"].values()), sum(changes[f"last {values[3]} mins"].values()), sum(changes[f"last {values[4]} mins"].values())))
    print(line , sep="", end = "\n")
    for i in range(len(sorted_names)):
        char_name = sorted_names[i]
        print('|{0:3s} | {1:20s} | {2:8d} | {3:10d} | {4:9d} | {5:6d} | {6:6d} | {7:7d} | {8:7d}'.format(f"{i+1}", char_name, total_rep[char_name], initial_rep[char_name], changes["total gain"][char_name], changes[f"last {values[1]} min"][char_name], changes[f"last {values[2]} mins"][char_name], changes[f"last {values[3]} mins"][char_name], changes[f"last {values[4]} mins"][char_name]))

def update_burnlist(burnlist, old_burnlist):
    change = {}
    for item in burnlist:
        change[item] = burnlist[item] - old_burnlist[item]
    return change

if __name__ == "__main__":
    start_players = get_reps()
    old_burntime = {}
    for i in values:
        old_burntime[i] = start_players.copy()
    names = ["total gain", "last 1 min"]
    names.extend([f"last {x} mins" for x in values[2:]])
    change = {}
    for name in names:
        change[name] = {k: 0 for k in old_burntime[values[0]]}
    counter = 0
    while True:
        time.sleep(60)
        counter += 1
        burnlist = get_reps()
        for i in range(len(values)):
            if counter % values[i] == 0 or i == 0:
                change[names[i]] = update_burnlist(burnlist, old_burntime[values[i]])
                if i != 0:
                    old_burntime[values[i]] = burnlist
        table(old_burntime[values[0]], burnlist, change)    
