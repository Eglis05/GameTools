from bs4 import BeautifulSoup
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from datetime import datetime
import csv

clan_id = 655 #RUH: 655
clan_name = "RUH"
availability_date = "2023-05-01"

one_interval = 30
values = [1000, 1, 2, 10, 20]
names = ["total gain", "last 30 secs", "last 1 min"]
names.extend([f"last {x//2} mins" for x in values[3:]])
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
link = "https://ninjasage.id/en/leaderboards/clan"
driver.get(link)
time.sleep(3)

dict_members = {}
if os.path.isfile("./members.csv"):
    with open('./members.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict_members[row["char_name"]] = row["fb_name"]
time.sleep(4)

def get_json(link):
    driver.get(link)
    time.sleep(7)
    driver.find_element(By.ID, "clan-row-" + str(clan_id)).find_element(By.CLASS_NAME, "pointer").click()
    time.sleep(3)
    driver.find_elements(By.XPATH, "//select/option[3]")[1].click()
    time.sleep(3)
    webp = driver.page_source
    soup = BeautifulSoup(webp, "html.parser")
    return soup.find_all("td")[93:]

def get_reps():
    ranks = get_json(link)
    members = {}
    for i in range(0, len(ranks), 6):
        name = ranks[i].text
        name = name[:name.find("[") - 1]
        while name in members.keys():
            name = name + " Jr."
        
        rep = int(ranks[i+2].text.replace(".", ""))
        members[name] = rep
    return members

def table(initial_rep, total_rep, changes):
    sorted_names = list(dict(sorted(changes[names[0]].items(), key=lambda item: item[1], reverse=True)).keys())
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')
    print('|{0:3s} | {1:20s} | {2:20s} | {3:10s} | {4:8s} | {5:9s} | {6:12s} | {7:10s} | {8:11s} | {9:11s}'.format("Pos", "Char Name", "FB NAME", "initialRep", "totalRep", "totalGain", names[1], names[2], names[3], names[4]), flush=True)
    line = "-" * 147
    print(line , sep="", end = "\n", flush=True)
    print('|{0:3d} | {1:20s} | {2:20s} | {3:10s} | {4:8s} | {5:9d} | {6:12d} | {7:10d} | {8:11d} | {9:11d}'.format(0, clan_name, "EGLIS", "SABI", "GAURAV", sum(changes["total gain"].values()), sum(changes[names[1]].values()), sum(changes[names[2]].values()), sum(changes[names[3]].values()), sum(changes[names[4]].values())), flush=True)
    print(line , sep="", end = "\n", flush=True)
    for i in range(len(sorted_names)):
        char_name = sorted_names[i]
        if char_name not in dict_members:
            dict_members[char_name] = ""
        print('|{0:3s} | {1:20s} | {2:20s} | {3:10d} | {4:8d} | {5:9d} | {6:12d} | {7:10d} | {8:11d} | {9:11d}'.format(f"{i+1}", char_name, dict_members[char_name], initial_rep[char_name], total_rep[char_name], changes["total gain"][char_name], changes[names[1]][char_name], changes[names[2]][char_name], changes[names[3]][char_name], changes[names[4]][char_name]), flush=True)
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
    if today_date >= datetime.strptime(availability_date, '%Y-%m-%d'):
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
            try:
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
            except:
                driver = webdriver.Chrome(options=options)