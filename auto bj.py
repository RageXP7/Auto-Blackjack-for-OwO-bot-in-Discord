import requests
import time
import json
import random
from playsound import playsound
import emoji
start = True
game = True
list1 = []
clock = [9,10,11]
default = 500
bet = default
bets = [500,500,500,500,500,500,500,1000]
username = ""

def bj(choice) :
    if choice == "punch" :
        punch()
    elif choice == "halt" :
        halt()
    elif choice == "lost" or choice == "won" :
        gameover(choice)
        
        
def punch() :
    global r
    global react_Punch
    if react_Punch == False :
        print("PUNCH : ",react_Punch )
        r = requests.put("https://discord.com/api/v9/channels/1094258368245411942/messages/{}/reactions/%F0%9F%91%8A/%40me?location=Message&burst=false".format(id),headers=header )
        react_Punch = True
    else :
        print("PUNCH : ",react_Punch )
        r = requests.delete("https://discord.com/api/v9/channels/1094258368245411942/messages/{}/reactions/%F0%9F%91%8A/%40me?location=Message".format(id),headers=header )
        react_Punch = False
def halt() :
    global r
    global react_Halt
    if react_Halt == False :
        print("HALT : ", react_Halt)
        r = requests.put("https://discord.com/api/v9/channels/1094258368245411942/messages/{}/reactions/%F0%9F%9B%91/%40me?location=Message&burst=false".format(id),headers=header )
        react_Halt = True
    else :
        print("HALT : ", react_Halt)
        r = requests.delete("https://discord.com/api/v9/channels/1094258368245411942/messages/{}/reactions/%F0%9F%9B%91/%40me?location=Message".format(id),headers=header )
        react_Halt = False
        
def gameover(x) :
    global bet
    if x == "lost" :
        bet = bet*2
        if bet > 120001 :
            bet = default
    elif x == "won" :
        bet = random.choice(bets)
    elif x == "draw" :
        print("draw")
        
def check() :
    global start
    l = requests.get("https://discord.com/api/v9/channels/1094258368245411942/messages", headers = header )
    log = json.loads(l.text)
    log = log[0]
    result = log['content']
    print(result)
    if "hajime" in result :
        global game
        start = True 
        game = True
        
header = {
        'authorization': "<>"
        }     

while(start == True) :        
    if game == True :
        react_Punch = False
        react_Halt = False
        time.sleep(random.choice(clock))
        message = {
        'content' : "owo bj {}".format(bet)
        }
        r = requests.post("https://discord.com/api/v9/channels/1094258368245411942/messages", data = message, headers = header )
        time.sleep(3) 
    print(game)  
    l = requests.get("https://discord.com/api/v9/channels/1094258368245411942/messages", headers = header )
    log = json.loads(l.text)
    result = str(log[0])
    print(result)
    if game == True :
        for num in range(8,27) :
            list1.append(result[num])
    game = False
    id = "".join(list1)
    print(id)
    if "human!" in result or "owo bj" in result :
        print("Caught Redhanded - ABORTING ")
        playsound("./DANGER.mp3")
        start = False
        while(start == False) :
            check()
            time.sleep(5)
            
    for i in range(1,16) :
        if f"'{username} `[{i}]`" in result or f"'{username} `[{i}]*`" in result:
            ch = "punch"
            bj(ch)
            id = ""
            time.sleep(2)
            break
    for i in range(16,22) :
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
    elif 'You won' in result :
        print("won")
        ch = "won"
        bj(ch) 
        game = True
        id = ""
        list1 = []
    elif "~ You tied!'" in result or "~ You both bust!" in result :
        print("draw")
        ch = "draw"
        bj(ch) 
        game = True
        id = ""
        list1 = []