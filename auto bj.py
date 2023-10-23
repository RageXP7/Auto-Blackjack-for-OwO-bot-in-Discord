import requests
import time
import json
import random
from playsound import playsound

# Configuration
start = True
game = True
list1 = []
clock = [9, 10, 11]
default = 500
bet = default
bets = [500, 500, 500, 500, 500, 500, 500, 1000]

#ToBeFilledByYou
username = ""
discord_channel_url = ""
header = {'authorization': ""}
audio_path = ""

# Functions for actions
def bj(choice):
    if choice == "punch":
        action("👊", "react_Punch")
    elif choice == "halt":
        action("🛑", "react_Halt")
    elif choice in ["lost", "won"]:
        gameover(choice)

def action(emoji, reaction_variable):
    global r
    global game
    if not globals()[reaction_variable]:
        print(f"{emoji} : {globals()[reaction_variable]}")
        r = requests.put(f"{discord_channel_url}/{id}/reactions/{emoji}/@me?location=Message&burst=false", headers=header)
        globals()[reaction_variable] = True
    else:
        print(f"{emoji} : {globals()[reaction_variable]}")
        r = requests.delete(f"{discord_channel_url}/{id}/reactions/{emoji}/@me?location=Message", headers=header)
        globals()[reaction_variable] = False

def gameover(x):
    global bet
    if x == "lost":
        bet = bet * 2
        if bet > 120001:
            bet = default
    elif x == "won":
        bet = random.choice(bets)
    elif x == "draw":
        print("draw")

# Check for "hajime" to start the game
def check_start():
    l = requests.get(discord_channel_url, headers=header)
    log = json.loads(l.text)
    result = log[0]['content']
    return "hajime" in result

while start:
    if game:
        react_Punch = False
        react_Halt = False
        time.sleep(random.choice(clock))
        message = {'content': f"owo bj {bet}"}
        r = requests.post(discord_channel_url, data=message, headers=header)
        time.sleep(3)

    l = requests.get(discord_channel_url, headers=header)
    log = json.loads(l.text)
    result = str(log[0])
    
    if game:
        list1 = result[8:27]

    game = False
    id = "".join(list1)

    if "human!" in result or f"owo bj {bet}" in result:
        print("Caught Redhanded - ABORTING")
        playsound(f"{audio_path}")
        start = False
        while not start:
            check_start()
            time.sleep(5)

    for i in range(1, 16):
        if f"'{username} `[{i}]`" in result or f"'{username} `[{i}]*`" in result:
            ch = "punch"
            bj(ch)
            id = ""
            time.sleep(2)
            break

    for i in range(16, 22):
        if f"'{username} `[{i}]`" in result or f"'{username} `[{i}]*`" in result:
            ch = "halt"
            bj(ch)
            id = ""
            time.sleep(2)
            break

    if 'You lost' in result:
        print("lost")
        ch = "lost"
        bj(ch)
        game = True
        id = ""
        list1 = []
    elif 'You won' in result:
        print("won")
        ch = "won"
        bj(ch)
        game = True
        id = ""
        list1 = []
    elif "~ You tied!'" in result or "~ You both bust!" in result:
        print("draw")
        ch = "draw"
        bj(ch)
        game = True
        id = ""
        list1 = []
