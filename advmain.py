from window import *
import math
import time
import random
import pickle
import os.path

#Initialisation des variables globales.
width = 0
height = 0
mapName = ""

LEFT = 37
UP = 38
RIGHT = 39
DOWN = 40
ENTER = 13

IMAGE_SIZE = 64

blocksWidth = 9
blocksHeight = 9

blocks = []
pnjs = []
triggers = {}

xOffset = 0
yOffset = 0

x = 3
y = 3

direction = "Up"
l = [False]

#DÃƒÂ©claration des blocs sous forme de constantes.

VOID_BLOCK = 0
GRASS_BLOCK = 1
GROUND_BLOCK = 2

DIRT_ROAD_UP = 10
DIRT_ROAD_DOWN = 11
DIRT_ROAD_LEFT = 12
DIRT_ROAD_RIGHT = 13
DIRT_ROAD_UP_TO_LEFT = 14
DIRT_ROAD_EDGE_UP_LEFT = 15

slots = ["helmet", "chest", "weapon", "boots"]
caracs = ["maxHP", "maxMP", "armor", "strength", "wisdom", "dexterity"]

#Dictionnaire vers les images des blocs
blockIndex = {VOID_BLOCK : "void.jpg", GRASS_BLOCK : "Herbe.jpg", GROUND_BLOCK : "plancher64.jpg", DIRT_ROAD_UP : "dirt_road_up.png", DIRT_ROAD_DOWN : "dirt_road_down.png", DIRT_ROAD_LEFT : "dirt_road_left.png", DIRT_ROAD_RIGHT : "dirt_road_right.png", DIRT_ROAD_UP_TO_LEFT : "dirt_road_up_to_left.png", DIRT_ROAD_EDGE_UP_LEFT : "dirt_road_edge_up_left.png"}

#Dictionnaire de soliditÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© des blocs
solidIndex = {VOID_BLOCK : True, GRASS_BLOCK: False, GROUND_BLOCK : False, DIRT_ROAD_UP : False, DIRT_ROAD_DOWN : FALSE, DIRT_ROAD_LEFT : False, DIRT_ROAD_RIGHT : False, DIRT_ROAD_UP_TO_LEFT : False, DIRT_ROAD_EDGE_UP_LEFT : False}

#Dictionnaire des ennemis - ChargÃƒÂ© depuis les fichiers
enemyIndex = {}

#Dictionnaire des objets - ChargÃƒÂ© depuis les fichiers
itemIndex = {}

#Dictionnaire reprÃƒÂ©sentant les caractÃƒÂ©ristiques de l'ennemi que l'on combat
estats = {}

#Dictionnaire reprÃƒÂ©sentant les caractÃƒÂ©ristiques du joueur - CaractÃ©ristiques de base.
stats = {"LVL" : 1, "XP" : 0, "maxHP" : 20, "HP" : 20, "maxMP" : 100, "MP" : 100, "strength" : 10, "wisdom" : 10, "dexterity" : 10, "armor" : 10, "items" : {"helmet" : "VOID", "chest" : "VOID" , "weapon" : "VOID", "boots" : "VOID"}, "inventory" : [], "skills" : ["strike"]}

#Variable globale utilisÃƒÂ©e en combat
myTurn = False

#Dictionnaire associant une image ÃƒÂ  un nom
images = {}

#Dictionnaire contenant les dialogues des diffÃƒÂ©rents pnjs
dialogs = {}

lastMove = 0

def playMusic(path):
    pass

def nothing():
    pass

def calcXP(lvl):
    return int( (900 / 99) * lvl * lvl + (9000 / 99) * lvl )

def lock():
    global l
    l[0] = False

def unlock():
    global l
    l[0] = True

def isLocked():
    global l
    return l[0]

def okMessage(callback):
    global txt, okButton
    txt.delete("all")
    okButton.destroy()
    callback()

def message(string, callback):
    global txt, okButton
    txt.delete("all")
    txt.create_text(10, 10, anchor = NW, text = string)
    okButton = Button(txt, text = "OK", command = lambda : okMessage(callback))
    okButton.place(x = 30, y = 50)

def updateFightScreen():
    global stats, estats, main, hishp, myhp, mymp

    hishp.config(value = estats["HP"])

    myhp.config(value = stats["HP"])

    mymp.config(value = stats["MP"])

    main.itemconfig(main.getvar("ehp"), text = "HP : " + str(estats["HP"]) + " / " + str(estats["maxHP"]))

    main.itemconfig(main.getvar("hp"), text = "HP : " + str(stats["HP"]) + " / " + str(stats["maxHP"]))

    main.itemconfig(main.getvar("mp"), text = "MP : " + str(stats["MP"]) + " / " + str(stats["maxMP"]))

    main.update()


def dealDamage(amount):
    global stats, estats, main, menu, hishp
    amount -= estats["armor"]
    if amount < 0:
        amount = 0
    estats["HP"] -= amount
    a = main.create_text(64, 64, text = str(int(amount)) + " !", tag="to_delete")
    updateFightScreen()

def takeDamage(amount):
    global stats, estats, main, txt, myhp
    amount -= stats["armor"]
    if amount < 0:
        amount = 0
    stats["HP"] -= amount
    main.create_text(448, 64, text = str(int(amount)) + " !", tag="to_delete")
    updateFightScreen()
    if stats["HP"] <= 0:
        print("Game OVER!") #TODO
        exit()

def dodgeTest():
    global stats, estats, myTurn, main
    if myTurn:
        if random.random() * estats["dexterity"] <= random.random() * stats["dexterity"]:
            return True
        else:
            a = main.create_text(64, 64, text = "DODGE !", tag="to_delete")
            main.update()
            return False
    else:
        if random.random() * estats["dexterity"] > random.random() * stats["dexterity"]:
            return True
        else:
            a = main.create_text(448, 64, text = "DODGE !", tag="to_delete")
            main.update()
            return False

def changeTurn():
    global myTurn, menu, turnCounter
    turnCounter += 1
    if myTurn:
        myTurn = False
        enemyAttack()
    else:
        myTurn = True
        displaySkills()

def clearTxt():
    global txt
    temp = []
    for key in txt.children.keys() :
        temp.append(txt.children[key])
    for child in temp:
        child.destroy()
        txt.update()

def clearMenu():
    global menu
    temp = []
    for key in menu.children.keys() :
        temp.append(menu.children[key])
    for child in temp:
        child.destroy()
        menu.update()

def clearMain():
    global main
    temp = []
    for key in main.children.keys() :
        temp.append(main.children[key])
    for child in temp:
        child.destroy()
        main.update()

def enemyAttack():
    global menu, estats, stats, skills, txt
    chosenSkill = random.choice(estats["skills"])
    txt.create_text(15,15,anchor = NW, text = "L'ennemi utilise : " + chosenSkill)
    skills[chosenSkill]()
    time.sleep(2)
    txt.delete("all")
    main.delete("to_delete")
    changeTurn()

def testLevelUp():
    global stats
    if stats["XP"] >= calcXP(stats["LVL"]):
        stats["XP"] -= calcXP(stats["LVL"])
        stats["LVL"] += 1
        stats["lvlPoints"] += 1
        message("LEVEL UP ! Niveau atteint : " + str(stats["LVL"]), testLevelUp)
    else:
        unlock()

def xp():
    global stats, estats, turnCounter
    bonusMultiplier = 1
    if turnCounter <= 4:
        bonusMultiplier = 1.2
    elif turnCounter <= 8:
        bonusMultiplier = 1.1
    gain = int( ( calcXP(estats["lvl"]) / 10 ) * bonusMultiplier * ( random.random() + 0.5 ))
    stats["XP"] += gain
    message("Vous gagnez : " + str(gain) + " XP !", testLevelUp)

def testLoot():
    global stats, estats
    pick = random.choice(estats["loot"])
    if pick != "VOID":
        inventoryAdd(pick)
        message("Vous trouvez : " + pick + " !", xp)
    else:
        xp()

def doSkill(skill):
    global stats, estats, skills, menu, txt, main
    txt.delete("all")
    txt.create_text(15, 15, anchor = NW, text = "Vous utilisez : " + skill)
    clearMenu()
    skills[skill]()
    time.sleep(2)
    txt.delete("all")
    main.delete("to_delete")
    if estats["HP"] <= 0:
        message("Vous ÃƒÂªtes victorieux !", testLoot)
        clearMain()
        showMenu()
        draw(xOffset,yOffset)

    else:
        changeTurn()

def zbra():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
             pass
    #        dealDamage(int(0.5 * stats["strength"] + 0.5 * stats["dexterity"]))
    else:
        if dodgeTest():
             pass
    #        takeDamage(0.5 * estats["strength"] + 0.5 * estats["dexterity"])


def strike():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest() and stats["MP"] >= 5:
            dealDamage(0.5 * stats["strength"] + 0.5 * stats["dexterity"])
    else:
        if dodgeTest():
            takeDamage(0.5 * estats["strength"] + 0.5 * estats["dexterity"])

skills = {"strike" : strike, "zbra" : zbra}

skillsDesc = {"strike" : {"MP" : "0" , "desc" : "Un coup de base."}, "zbra" : {"MP" : "0", "desc" : "LOL TEST"}}

def titleToGame():
    global c
    c.destroy()
    unlock()

def displayDesc(skill):
    global txt, skillsDesc
    txt.delete('all')
    txt.create_text(5,5, text = skill, anchor = NW)
    txt.create_text(5, 20, text = skillsDesc[skill]["MP"] + " MP", anchor = NW)
    txt.create_text(5, 35, text = skillsDesc[skill]["desc"], anchor = NW)

def displaySkills(offset = 0):
    global menu, txt, upb, downb, stats, estats, skills
    clearMenu()
    nbskills = len(stats["skills"])
    yo = 84
    if nbskills < 6:
        for skill in stats["skills"]:
            b = Button(menu, text = skill, command = lambda skill = skill : doSkill(skill))
            b.place(x = 10, y = yo, width = 108, height = 64)
            b.bind("<Enter>", lambda e : displayDesc(skill))
            b.bind("<Leave>", lambda e : txt.delete("all"))
            yo += 64 + 10
    else:
        if offset < 0:
            offset = 0
        elif offset > nbskills - 5:
            offset = nbskills - 5

        upb = Button(menu, text = "UP", command = lambda : displaySkills(offset = offset - 1))
        upb.place(x = 10, y = 10, width = 108, height = 64)
        downb = Button(menu, text = "DOWN", command = lambda : displaySkills(offset = offset + 1))
        downb.place(x = 10, y = 502, width = 108, height = 64)

# Mise en place...
        for i in range(offset, offset + 5):
            b = Button(menu, text = stats["skills"][i], command = lambda i = i: doSkill(stats["skills"][i]))
            b.place(x = 10, y = yo, width = 108, height = 64)
            b.bind("<Enter>", lambda e, i = i: displayDesc(stats["skills"][i]))
            b.bind("<Leave>", lambda e , i = i: txt.delete("all"))
            yo += 64 + 10

def load():
    global stats, x ,y, xOffset, yOffset, mapName, direction, images

    f = open("test.save","rb")

    tx = pickle.load(f)
    ty = pickle.load(f)
    tdirection = pickle.load(f)
    stats = pickle.load(f)
    mapName = pickle.load(f)

    loadResources(open(mapName + ".level", "r"))

    x = tx
    y = ty
    xOffset = x - 4
    yOffset = y - 4

    direction = tdirection

    images["player"] = images[direction]

    f.close()

def save():
    global x, y, stats, mapName, direction

    lock()

    f = open("test.save","wb")

    pickle.dump(x,f)
    pickle.dump(y,f)
    pickle.dump(direction, f)
    pickle.dump(stats,f)
    pickle.dump(mapName,f)

    f.close()

    unlock()

def back():
    global txt
    txt.delete("all")
    clearTxt()
    showMenu()
    unlock()

def attribPoint(stat):
    global stats
    stats["lvlPoints"] -= 1
    stats[stat] += 1
    txt.delete("all")
    clearTxt()
    displayChar()

def displayChar():
    global txt, stats

    lock()

    clearMenu()

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground = 'red', background = 'red')

    s2 = ttk.Style()
    s2.theme_use('clam')
    s2.configure("cyan.Horizontal.TProgressbar", foreground = 'cyan', background = 'cyan')

    s3 = ttk.Style()
    s3.theme_use('clam')
    s3.configure("green.Horizontal.TProgressbar", foreground = "green", background = "green")

    txt.create_text(15, 15, text = "Name : ", anchor = NW)

    txt.create_text(15, 35, text = "Strength : " + str(stats["strength"]), anchor = NW)
    txt.create_text(15, 55, text = "Wisdom : " + str(stats["wisdom"]), anchor = NW)
    txt.create_text(15, 75, text = "Dexterity : " + str(stats["dexterity"]), anchor = NW)
    txt.create_text(15, 95, text = "Armor : " + str(stats["armor"]), anchor = NW)

    if stats["lvlPoints"] != 0:
        txt.create_text(150, 15, text = "Points Ã  dÃ©penser : " + str(stats["lvlPoints"]), anchor = NW)
        b = Button(txt, text = "+ Strength", command = lambda i = "strength" : attribPoint(i))
        b.place(x = 150, y = 35, height = 20, width = 64)
        b = Button(txt, text = "+ Widsom", command = lambda i = "wisdom" : attribPoint(i))
        b.place(x = 150, y = 55, height = 20, width = 64)
        b = Button(txt, text = "+ Dexterity", command = lambda i = "dexterity" : attribPoint(i))
        b.place(x = 150, y = 75, height = 20, width = 64)

    txt.create_text(300, 15, text = "LVL : " + str(stats["LVL"]), anchor = NW)

    exp = ttk.Progressbar(txt, orient = "horizontal", mode = "determinate", length = 50, maximum = calcXP(stats["LVL"]), value = stats["XP"], style = "green.Horizontal.TProgressbar")
    exp.place(x = 300, y = 35)

    txt.create_text(300, 55, text = "XP : " + str(stats["XP"]) + " / " + str(calcXP(stats["LVL"])), anchor = NW)

    hp = ttk.Progressbar(txt, orient = "horizontal", mode = "determinate", length = 100, maximum = stats["maxHP"], value = stats["HP"], style = "red.Horizontal.TProgressbar")
    hp.place(x = 400, y = 15, anchor = NW)

    txt.create_text(400, 35, text = "HP : " + str(stats["HP"]) + " / " + str(stats["maxHP"]), anchor = NW)

    mp = ttk.Progressbar(txt, orient = "horizontal", mode = "determinate", length = 100, maximum = stats["maxMP"], value = stats["MP"], style = "cyan.Horizontal.TProgressbar")
    mp.place(x = 400, y = 55, anchor = NW)

    txt.create_text(400, 75, text = "MP : " + str(stats["MP"]) + " / " + str(stats["maxMP"]), anchor = NW)

    b = Button(txt, text = "Retour", command = back)
    b.place(x = 550, y = 60, width = 108, height = 64)

def inventoryEquip(item): # Fonction pour Ã©quiper un objet  depuis l'inventaire
    global stats, itemIndex
    if stats["items"][itemIndex[item]["slot"]] != "VOID": #Si on a dÃ©jÃ  un objet Ã©quipÃ© dans cet emplacement, on le dÃ©sÃ©quipe
        unequip(stats["items"][itemIndex[item]["slot"]])
    equip(item) # On Ã©quipe l'objet
    clearTxt() # On efface la zone de texte
    displayInventory() #Et on rÃ©affiche l'inventaire

def invToMenu():
    global txt
    txt.delete("all")
    clearMenu()
    showMenu()

def pickItem(item):
    global itemIndex, slots, txt, caracs
    yo = 10
    if itemIndex[item]["slot"] in slots:
        b = Button(txt, text = "EQUIP", command = lambda i = item : inventoryEquip(i))
        b.place(x = 350, y = 10, width = 108, height = 64)
        for a in itemIndex[item]:
            if a in caracs:
                txt.create_text(200, yo, text = a + " : " + str(itemIndex[item][a]), anchor = NW)
                yo += 15
    yo = 10
    for t in itemIndex[item]["desc"]:
        txt.create_text(10, yo, text = t, anchor = NW)
        yo += 15

def displayInventory(offset = 0):
    global txtt, menu, stats
    clearMenu()
    txt.delete("all")
    if len(stats["inventory"]) == 0:
        showMenu()
        return
    elif len(stats["inventory"]) < 5:
        yo = 84
        for item in stats["inventory"].keys():
            b = Button(menu, text = item + " x " + str(stats["inventory"][item]), command = lambda i = item : pickItem(i))
            b.place(x = 10, y = yo, height = 64, width = 108)
            yo += 74
    else:
        if offset + 4 > len(stats["inventory"]):
            offset -= 1
        elif offset < 0:
            offset = 0
        up = Button(menu, text = "UP", command = lambda o = offset - 1 : displayInventory(offset = o))
        up.place(x = 10, y = 10, height = 64, width = 108)
        down = Button(menu, text = "DOWN", command = lambda o = offset + 1 : displayInventory(offset = o))
        down.place(x = 10, y = 10 + 5 * 74, height = 64, width = 108)
        yo = 84
        for i in range(offset, offset + 4):
            b = Button(menu, text = list(stats["inventory"].keys())[i] + "x" + str(stats["inventory"][list(stats["inventory"].keys())[i]]), command = lambda i = list(stats["inventory"].keys())[i] : pickItem(i))
            b.place(x = 10, y = yo, width = 108, height = 64)
            yo += 74
    b = Button(menu, text = "RETURN", command = invToMenu)
    b.place(x = 10, y = 10 + 6 * 74, width = 108, height = 64)

def equipmentUnequip(item):
    global stats, itemIndex, txt
    stats["items"][itemIndex[item]["slot"]] = "VOID"
    inventoryAdd(item)
    clearMenu()
    txt.delete('all')
    clearTxt()
    displayEquipment()

def pickEquipment(item):
    global itemIndex, stats
    yo = 10
    b = Button(txt, text = "UNEQUIP", command = lambda i = item : equipmentUnequip(i))
    b.place(x = 350, y = 10, width = 108, height = 64)
    for a in itemIndex[item]:
        if a in caracs:
            txt.create_text(200, yo, text = a + " : " + str(itemIndex[item][a]), anchor = NW)
            yo += 15
    yo = 10
    for t in itemIndex[item]["desc"]:
        txt.create_text(10, yo, text = t, anchor = NW)
        yo += 15

def displayEquipment():
    global stats, menu
    clearMenu()
    yo = 10
    for slot in list(stats["items"].keys()):
        if stats["items"][slot] == "VOID":
            b = Button(menu, text = slot + " :\nVIDE")
            b.place(x = 10, y = yo, width = 108, height = 64)
        else:
            b = Button(menu, text = slot + "\n" + stats["items"][slot], command = lambda i = stats["items"][slot] : pickEquipment(i) )
            b.place(x = 10, y = yo, width = 108, height = 64)
        yo += 74
    q = Button(menu, text = "RETURN", command = invToMenu)
    q.place(x = 10, y = 306, width = 108, height = 64)

def showMenu():
    global menu
    c = Button(menu, text = "Perso", command = displayChar)
    c.place(x = 10, y = 10, width = 108, height = 64)
    i = Button(menu, text = "Inventaire", command = displayInventory)
    i.place(x = 10, y = 84, width = 108, height = 64)
    s = Button(menu, text = "Sauvegarder", command = save)
    s.place(x = 10, y = 158, width = 108, height = 64)
    e = Button(menu, text = "Equipement", command = displayEquipment)
    e.place(x = 10, y = 232, width = 108, height = 64)

def fightScreen(name):
    global main, images, myTurn, myhp, mymp, hishp, stats, estats

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground = 'red', background = 'red')

    s2 = ttk.Style()
    s2.theme_use('clam')
    s2.configure("cyan.Horizontal.TProgressbar", foreground = 'cyan', background = 'cyan')

    myhp = ttk.Progressbar(main, orient = "horizontal", mode = "determinate", length = 172, maximum = stats["maxHP"], value = stats["HP"], style = "red.Horizontal.TProgressbar")
    myhp.place(x = 394, y = 200, anchor = NW)

    mymp = ttk.Progressbar(main, orient = "horizontal", mode = "determinate", length = 172, maximum = stats["maxMP"], value = stats["MP"], style = "cyan.Horizontal.TProgressbar")
    mymp.place(x = 394, y = 240, anchor = NW)

    hishp = ttk.Progressbar(main, orient = "horizontal", mode = "determinate", length = 172, maximum = estats["maxHP"], value = estats["HP"], style = "red.Horizontal.TProgressbar")
    hishp.place(x = 10, y = 200, anchor = NW)

    main.create_image(0,0,anchor = NW, image = images["fight_background"])
    main.create_image(0,0, anchor = NW, image = images[name])
    main.create_image(384, 0, anchor = NW, image = images["fight_image"])

    a = main.create_text(10, 220, text = "HP : " + str(estats["HP"]) + " / " + str(estats["maxHP"]), anchor = NW)

    b = main.create_text(394, 260, text = "MP : " + str(stats["MP"]) + " / " + str(stats["maxMP"]), anchor = NW)

    c = main.create_text(394, 220, text = "HP : " + str(stats["HP"]) + " / " + str(stats["maxHP"]), anchor = NW)

    main.setvar(name = "ehp", value = a)
    main.setvar(name = "mp", value = b)
    main.setvar(name = "hp", value = c)

    if random.random() * estats["dexterity"] <= stats["dexterity"]:
        myTurn = True
        message("Vous commencez !", displaySkills)
    else:
        myTurn = False
        message(name + " commence !", enemyAttack)

def fight(name):
    global main, txt, estats, menu, stats, turnCounter
    lock()
    turnCounter = 1
    main.delete("all")
    clearMenu()
    for key in enemyIndex[name].keys():
         estats[key] = enemyIndex[name][key]
    message("Combat contre un : " + name, lambda : fightScreen(name))

def pnjDialog(canvas, name):
    global dialogs
    if len(dialogs[name]) != 0:
        dialog(canvas, dialogs[name], unlock)
    else:
        unlock()

def blockAction(block):
  global stats
  if block == VOID_BLOCK:
    playMusic('test.wav')
    message("LE CHAMPOMY C'EST POUR LES FAIBLES !", unlock)

def triggerAction(x , y, name):
  global width, blocks, pnjs, triggers, main, dialogs, enemyIndex
  if name.startswith("FIGHT:"):
      if random.random() <= 1 / enemyIndex[name[len("FIGHT:"):]]["proba"]:
          fight(name[len("FIGHT:"):])
  elif name.startswith("LOAD:"):
    lock()
    blocks = []
    pnjs = []
    triggers = {}
    dialogs = {}
    main.delete('all')
    loadResources(open(name[len("LOAD:"):],'r'))
    unlock()
  elif name.startswith("MESSAGE:"):
    lock()
    message(name[len("MESSAGE:"):], unlock)

def createMap(f):
  global width, height, blocks, pnjs, x, y, xOffset, yOffset, mapName
  line = f.readline().rstrip("\n")
  mapName = f.readline().rstrip("\n")
  fbg = f.readline().rstrip("\n")
  images["fight_background"] = loadImage(fbg)
  width = int(f.readline().rstrip("\n"))
  height = int(f.readline().rstrip("\n"))
  x = int(f.readline().rstrip("\n"))
  y = int(f.readline().rstrip("\n"))
  xOffset = x - 4
  yOffset = y - 4
  a = 1
  b = 0
  line = f.readline().rstrip("\n")
  while line != "}":
    for l in line:
      if a < 3:
        b += int(int(l) * math.pow(10, -1 * a + 3))
        a += 1
      else:
        b += int(l)
        blocks.append(b)
        b = 0
        a = 1
    line = f.readline().rstrip("\n")
  for temp in range(width * height):
    pnjs.append(-1)
    triggers[temp] = []

def createPNJ(f):
  global pnjs, width, images, dialogs
  line = f.readline().rstrip("\n")
  name = f.readline().rstrip("\n")
  ipath = f.readline().rstrip("\n")
  path = f.readline().rstrip("\n")
  x = int(f.readline().rstrip("\n"))
  y = int(f.readline().rstrip("\n"))
  pnjs[x + y * width] = name
  images[name] = loadImage(ipath)
  file = open(path, "r")
  dialogs[name] = file.readlines()
  file.close()
  line = f.readline().rstrip("\n")

def createTrigger(f):
  global triggers, width
  line = f.readline().rstrip("\n")
  name = f.readline().rstrip("\n")
  x = int(f.readline().rstrip("\n"))
  y = int(f.readline().rstrip("\n"))
  triggers[x + y * width].append(name)
  line = f.readline().rstrip("\n")

def loadItem(f):
    global itemIndex
    line = f.readline().rstrip("\n")
    name = f.readline().rstrip("\n")
    itemIndex[name] = {}
    line = f.readline().rstrip("\n")
    while line != "[DESC]":
        try:
            itemIndex[name][line[:line.find(":")]] = int(line[line.find(":") + 1:])
        except:
            itemIndex[name][line[:line.find(":")]] = line[line.find(":") + 1:]
        line = f.readline().rstrip("\n")
    line = f.readline().rstrip("\n")
    line = f.readline().rstrip("\n")
    itemIndex[name]["desc"] = []
    while line != "}":
        itemIndex[name]["desc"].append(line)
        line = f.readline().rstrip("\n")

def loadEnemy(f):
    global enemyIndex, images
    line = f.readline().rstrip("\n") # {
    name = f.readline().rstrip("\n") # NOM
    enemyIndex[name] = {}
    image = f.readline().rstrip("\n") # IMAGE
    images[name] = loadImage(image)
    line = f.readline().rstrip("\n") # CARACTERISTIQUES
    while line != "[SKILLS]":
        try :
            enemyIndex[name][line[:line.find(":")]] = int(line[line.find(":") + 1:])
        except ValueError:
            enemyIndex[name][line[:line.find(":")]] = line[line.find(":") + 1:]
        line = f.readline().rstrip("\n")
    line = f.readline().rstrip("\n") # {
    line = f.readline().rstrip("\n") # SKILLS
    enemyIndex[name]["skills"] = []
    while line != "}":
        enemyIndex[name]["skills"].append(line)
        line = f.readline().rstrip("\n")
    line = f.readline().rstrip("\n") # [LOOT]
    line = f.readline().rstrip("\n") # {
    line = f.readline().rstrip("\n") # LOOT
    enemyIndex[name]["loot"] = []
    while line != "}":
        enemyIndex[name]["loot"].append(line)
        line = f.readline().rstrip("\n")
    line = f.readline().rstrip("\n") # }

def loadResources(f):
  global blocks, blockIndex, images
  line = f.readline().rstrip("\n")
  if line == "[MAP]":
    createMap(f)
  elif line == "[PNJ]":
    createPNJ(f)
  elif line == "[TRIGGER]":
    createTrigger(f)
  elif line == "[ENEMY]":
    loadEnemy(f)
  elif line == "[ITEM]":
    loadItem(f)
  if line != '':
    loadResources(f)
  for block in blocks:
    images[block] = loadImage(blockIndex[block])

def inventoryAdd(name):
    global stats
    if name in stats["inventory"].keys():
        stats["inventory"][name] += 1
    else:
        stats["inventory"][name] = 1

def inventoryRemove(name):
    global stats
    stats["inventory"][name] -= 1
    if stats["inventory"][name] == 0:
        stats["inventory"].pop(name, None)

def check():
    global stats
    if stats["HP"] > stats["maxHP"]:
        stats["HP"] = stats["maxHP"]
    if stats["MP"] > stats["maxMP"]:
        stats["MP"] = stats["maxMP"]

def equip(name):
    global stats, itemIndex, caracs, slots
    if itemIndex[name]["slot"] in slots:
        if stats["items"][itemIndex[name]["slot"]] == "VOID":
            stats["items"][itemIndex[name]["slot"]] = name
            inventoryRemove(name)
            for key in itemIndex[name].keys():
                if key in caracs:
                    stats[key] += itemIndex[name][key]
            check()

def unequip(name):
    global stats, itemIndex, caracs
    if name in stats["items"].values():
        stats["items"][itemIndex[name]["slot"]] = "VOID"
        inventoryAdd(name)
        for key in itemIndex[name].keys():
            if key in caracs:
                stats[key] -= itemIndex[name][key]
        check()


def keyListener(event):
  global LEFT, RIGHT, UP, DOWN, ENTER,blocksWidth, blocksHeight, x , y, direction, width, height, blocks, pnjs, triggers, xOffset, yOffset, txt, lastMove
  if isLocked() == True:
    a = event.keycode
    vx = 0
    vy = 0
    if a == LEFT and x > 0:
      vx -= 1
      direction = "Left"
      images["player"] = images["Left"]
    elif a == RIGHT and x < width - 1:
      vx += 1
      direction = "Right"
      images["player"] = images["Right"]
    if a == DOWN and y < height - 1:
      vy += 1
      direction = "Down"
      images["player"] = images["Down"]
    elif a == UP and y > 0:
      vy -= 1
      direction = "Up"
      images["player"] = images["Up"]
    if (vx != 0 or vy != 0) and solidIndex[blocks[ x + vx + ( y + vy ) * width]] == False and pnjs[x + vx + ( y + vy ) * width] == -1 and (time.time() - lastMove >= 1 / 10):
      x += vx
      y += vy
      xOffset += vx
      yOffset += vy
      lastMove = time.time()
      for trigger in triggers[x + y * width]:
        triggerAction(x, y, trigger)
    if a == ENTER:
      if direction == "Left":
        vx = -1
      elif direction == "Right":
        vx = 1
      elif direction == "Up":
        vy = -1
      else:
        vy = 1
      if x + vx > -1 and x + vx < width and y + vy > -1 and y + vy < height:
        if pnjs[x + vx + ( y + vy ) * width] != -1:
          lock()
          pnjDialog(txt, pnjs[x + vx + ( y + vy ) * width])
        else:
          blockAction(blocks[x + vx + ( y + vy ) * width])
    draw(xOffset,yOffset)

createWindow(keyListener)

images["Background"] = loadImage("background.png")

images["Up"] = loadImage("up.png")
images["Down"] = loadImage("down.png")
images["Left"] = loadImage("left.png")
images["Right"] = loadImage("right.png")

images["fight_image"] = loadImage("gentil.png")

main, txt, menu = gameCanvas()

showMenu()

c = titleMenu(titleToGame, images["Background"])

def draw(xOffset, yOffset):
  global width, height, main, x, y, pnjs, images, blocks, IMAGE_SIZE, blocksWidth, blocksHeight

  main.delete("all")
  xC = 0
  yC = 0

  if xOffset < 0:
    xC = -1 * xOffset
  elif xOffset + blocksWidth > width:
    xC = -1 * (xOffset + blocksWidth - width)
  if yOffset < 0:
    yC = -1 * yOffset
  elif yOffset + blocksHeight > height:
    yC = - 1 * (yOffset + blocksHeight - height)

  for a in range(xOffset, xOffset + blocksWidth):
    for b in range(yOffset, yOffset + blocksHeight):
      xPos = (a + xC - xOffset) * IMAGE_SIZE
      yPos = (b + yC - yOffset) * IMAGE_SIZE
      main.create_image(xPos, yPos, anchor = NW, image = images[blocks[(a + xC) + (b + yC) * width]])

  for a in range(xOffset, xOffset + blocksWidth):
    for b in range(yOffset, yOffset + blocksHeight):
      xPos = (a + xC - xOffset) * IMAGE_SIZE
      yPos = (b + yC - yOffset) * IMAGE_SIZE
      if pnjs[(a + xC) + (b + yC) * width] != -1:
        main.create_image(xPos, yPos, anchor = NW, image = images[pnjs[(a + xC) + (b + yC) * width]])

  main.create_image((x - xOffset) * IMAGE_SIZE, (y - yOffset) * IMAGE_SIZE, anchor = NW, image = images["player"])

f = open('items.txt', 'r')
loadResources(f)
f.close()

if os.path.exists("test.save"):
    load()
else:
    stats = {"LVL" : 1, "XP" : 0, "lvlPoints" : 0, "maxHP" : 20, "HP" : 20, "maxMP" : 100, "MP" : 100, "strength" : 10, "wisdom" : 10, "dexterity" : 10, "armor" : 0, "items" : {"helmet" : "VOID", "chest" : "VOID" , "weapon" : "VOID", "boots" : "VOID"}, "inventory" : [], "skills" : ["strike"]}
    f = open('level1.level','r')
    loadResources(f)
    f.close()

draw(xOffset, yOffset)

runWindow()
