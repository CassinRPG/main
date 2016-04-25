from window import *
import math
import time
import random
import pickle
import os.path

#Initialisation des variables

#Taille de la map
width = 0
height = 0
mapName = ""

#Code des touches
LEFT = 37
UP = 38
RIGHT = 39
DOWN = 40
ENTER = 13

#Taille des images
IMAGE_SIZE = 64

#Nombre de blocs à l'écran
blocksWidth = 9
blocksHeight = 9

#Tableaux représentant la carte
blocks = []
pnjs = []
triggers = {}

#Offset caméra
xOffset = 0
yOffset = 0

#Coordonnées du joueur
x = 3
y = 3

#direction du joueur
direction = "Up"

#Variable permettant de lock
l = [False]

#Déclaration des blocs sous forme de constantes.
VOID_BLOCK = 0

GRASS = 1

DIRT = 2

PATH_GRASS_VERTICAL = 3

PATH_GRASS_HORIZONTAL = 4

PATH_GRASS_HVD = 5

PATH_GRASS_HVG = 6

PATH_GRASS_BVD = 7

PATH_GRASS_BVG = 8

PATH_DIRT_VERTICAL = 9

PATH_DIRT_HORIZONTAL = 10

PATH_DIRT_HVD = 11

PATH_DIRT_HVG = 12

PATH_DIRT_BVD = 13

PATH_DIRT_BVG = 14

TREE_1 = 15

TREE_2 = 16

ROCK_GRASS = 17

ROCK_DIRT = 18

GRASS_HOUSE_1 = 19

GRASS_HOUSE_2 = 20

GRASS_HOUSE_3 = 21

GRASS_HOUSE_4 = 22

GRASS_HOUSE_5 = 23

GRASS_HOUSE_6 = 24

GRASS_HOUSE_7 = 25

GRASS_HOUSE_8 = 26

GRASS_HOUSE_9 = 27

FLOOR = 28

TABLE_1 = 29

TABLE_2 = 30

TABLE_3 = 31

TABLE_4 = 32

PILLOW = 33

SHELF_SMALL = 34

FLOWER = 35

GTORCHED_TREE1 = 36

GTORCHED_TREE2 = 37

DTORCHED_TREE1 = 38

DTORCHED_TREE2 = 39

TRAN_DG_1 = 40

TRAN_DG_2 = 41

TRAN_DG_3 = 42

TRAN_DG_4 = 43

TRAN_GD_1 = 44

TRAN_GD_2 = 45

TRAN_GD_3 = 46

TRAN_GD_4 = 47

TRAN_HOR1 = 48

TRAN_HOR2 = 49

TRAN_VER1 = 50

TRAN_VER2 = 51

END_D = 52

END_G = 53

END_H = 54

END_B = 55

PATH_GRASS_BDG = 56

PATH_GRASS_BHG = 57

PATH_GRASS_BDH = 58

PATH_GRASS_HDG = 59

PATH_GRASS_BHGD = 60

CHEST = 400

OPEN_CHEST = 401

ROCK_WALL = 403

ROCK_FLOOR = 404

ROCK_CIRCLE_NW = 405

ROCK_CIRCLE_N = 406

ROCK_CIRCLE_NE = 407

ROCK_CIRCLE_W = 408

ROCK_CIRCLE_C = 409

ROCK_CIRCLE_E = 410

ROCK_CIRCLE_SW = 411

ROCK_CIRCLE_S = 412

ROCK_CIRCLE_SE = 413


#Tableaux décrivant les emplacements/caractéristiques
slots = ["helmet", "chest", "weapon", "boots"]
caracs = ["maxHP", "maxMP", "armor", "strength", "wisdom", "dexterity"]

#Dictionnaire vers les images des blocs
blockIndex = {VOID_BLOCK : "VOID.jpg", GRASS : "GRASS.jpg", DIRT : "DIRT.jpg", PATH_GRASS_VERTICAL : "PATH_GRASS_VERTICAL.jpg", PATH_GRASS_HORIZONTAL : "PATH_GRASS_HORIZONTAL.jpg", PATH_GRASS_HVD : "PATH_GRASS_HVD.jpg", PATH_GRASS_HVG : "PATH_GRASS_HVG.jpg", PATH_GRASS_BVD : "PATH_GRASS_BVD.jpg", PATH_GRASS_BVG : "PATH_GRASS_BVG.jpg", PATH_DIRT_VERTICAL : "PATH_DIRT_VERTICAL.jpg", PATH_DIRT_HORIZONTAL : "PATH_DIRT_HORIZONTAL.jpg", PATH_DIRT_HVD : "PATH_DIRT_HVD.jpg", PATH_DIRT_HVG : "PATH_DIRT_HVG.jpg", PATH_DIRT_BVD : "PATH_DIRT_BVD.jpg", PATH_DIRT_BVG : "PATH_DIRT_BVG.jpg", TREE_1 : "TREE_1.jpg", TREE_2 : "TREE_2.jpg", ROCK_GRASS : "ROCK_GRASS.jpg", ROCK_DIRT : "ROCK_DIRT.jpg", GRASS_HOUSE_1 : "GRASS_HOUSE_1.jpg", GRASS_HOUSE_2 : "GRASS_HOUSE_2.jpg", GRASS_HOUSE_3 : "GRASS_HOUSE_3.jpg", GRASS_HOUSE_4 : "GRASS_HOUSE_4.jpg", GRASS_HOUSE_5 : "GRASS_HOUSE_5.jpg", GRASS_HOUSE_6 : "GRASS_HOUSE_6.jpg", GRASS_HOUSE_7 : "GRASS_HOUSE_7.jpg", GRASS_HOUSE_8 : "GRASS_HOUSE_8.jpg", GRASS_HOUSE_9 : "GRASS_HOUSE_9.jpg", FLOOR : "FLOOR.jpg", TABLE_1 : "TABLE_1.jpg", TABLE_2 : "TABLE_2.jpg", TABLE_3 : "TABLE_3.jpg", TABLE_4 : "TABLE_4.jpg", PILLOW : "PILLOW.jpg", SHELF_SMALL : "SHELF_SMALL.jpg", FLOWER : "FLOWER.jpg", CHEST : "CHEST.png", GTORCHED_TREE1 : "GTORCHED_TREE1.jpg", GTORCHED_TREE2 : "GTORCHED_TREE2.jpg", DTORCHED_TREE1 : "DTORCHED_TREE1.jpg", DTORCHED_TREE2 : "DTORCHED_TREE2.jpg", TRAN_DG_1 : "TRAN_DG_1.jpg", TRAN_DG_2 : "TRAN_DG_2.jpg", TRAN_DG_3 : "TRAN_DG_3.jpg", TRAN_DG_3 : "TRAN_DG_3.jpg", TRAN_GD_1 : "TRAN_GD_1.jpg", TRAN_GD_2 : "TRAN_GD_2.jpg", TRAN_GD_3 : "TRAN_GD_3.jpg", TRAN_GD_3 : "TRAN_GD_3.jpg", TRAN_HOR1 : "TRAN_HOR1.jpg", TRAN_HOR2 : "TRAN_HOR2.jpg", TRAN_VER1 : "TRAN_VER1.jpg", TRAN_VER2 : "TRAN_VER2.jpg", END_D : "END_D.jpg", END_G : "END_G.jpg", END_H : "END_H.jpg", END_B : "END_B.jpg", PATH_GRASS_BDG : "PATH_GRASS_BDG.jpg", PATH_GRASS_BHG : "PATH_GRASS_BHG.jpg", PATH_GRASS_BDH : "PATH_GRASS_BDH.jpg", PATH_GRASS_HDG : "PATH_GRASS_HDG.jpg", PATH_GRASS_BHGD : "PATH_GRASS_BHGD.jpg", OPEN_CHEST : "OPEN_CHEST.png", ROCK_CIRCLE_NW : "CIRCLE_NW.png", ROCK_CIRCLE_N : "CIRCLE_N.png", ROCK_CIRCLE_NE : "CIRCLE_NE.png", ROCK_CIRCLE_W : "CIRCLE_W.png", ROCK_CIRCLE_C : "CIRCLE_C.png", ROCK_CIRCLE_E : "CIRCLE_E.png", ROCK_CIRCLE_SW : "CIRCLE_SW.png", ROCK_CIRCLE_S : "CIRCLE_S.png", ROCK_CIRCLE_SE : "CIRCLE_SE.png"}

#Dictionnaire de solidité des blocs
solidIndex = {VOID_BLOCK : True, GRASS : False, DIRT : False, PATH_GRASS_VERTICAL : False, PATH_GRASS_HORIZONTAL : False,PATH_GRASS_HVD : False, PATH_GRASS_HVG : False, PATH_GRASS_BVD : False, PATH_GRASS_BVG : False, PATH_DIRT_VERTICAL : False, PATH_DIRT_HORIZONTAL : False, PATH_DIRT_HVD : False, PATH_DIRT_HVG : False, PATH_DIRT_BVD : False, PATH_DIRT_BVG : False, TREE_1 : True, TREE_2 : True, ROCK_GRASS : True, ROCK_DIRT : True, GRASS_HOUSE_1 : True, GRASS_HOUSE_2 : True, GRASS_HOUSE_3 : True, GRASS_HOUSE_4 : True, GRASS_HOUSE_5 : True, GRASS_HOUSE_6 : True, GRASS_HOUSE_7 : True, GRASS_HOUSE_8 : True, GRASS_HOUSE_9 : True, FLOOR : False, TABLE_1 : True, TABLE_2 : True, TABLE_3 : True, TABLE_4 : True, PILLOW : True, SHELF_SMALL : True, FLOWER : True , CHEST: True, GTORCHED_TREE1 : True, GTORCHED_TREE2 : True, DTORCHED_TREE1 : True, DTORCHED_TREE2 : True, TRAN_DG_1 : False, TRAN_DG_2 : False, TRAN_DG_3 : False, TRAN_DG_4 : False, TRAN_GD_1 : False, TRAN_GD_2 : False, TRAN_GD_3 : False, TRAN_GD_4 : False, TRAN_HOR1 : False, TRAN_HOR2 : False, TRAN_VER1 : False, TRAN_VER2 : False, END_D : False, END_G : False, END_H : False, END_B : False, PATH_GRASS_BDG : False, PATH_GRASS_BHG : False, PATH_GRASS_BDH : False, PATH_GRASS_HDG : False, PATH_GRASS_BHGD : False, OPEN_CHEST : True, ROCK_WALL : True, ROCK_FLOOR : False, ROCK_CIRCLE_NW : False, ROCK_CIRCLE_N : False, ROCK_CIRCLE_NE : False, ROCK_CIRCLE_W : False, ROCK_CIRCLE_C : False, ROCK_CIRCLE_E : False, ROCK_CIRCLE_SW : False, ROCK_CIRCLE_S : False, ROCK_CIRCLE_SE : False}

#Dictionnaire des ennemis - Chargé depuis les fichiers
enemyIndex = {}

#Dictionnaire des objets - Chargé depuis les fichiers
itemIndex = {}

#Dictionnaire repréristiques de l'ennemi que l'on combat
estats = {}

#Dictionnaire représentant les caractéristiques du joueur - Caractéristiques de base.
stats = {"LVL" : 1, "XP" : 0, "maxHP" : 20, "HP" : 20, "maxMP" : 100, "MP" : 100, "strength" : 10, "wisdom" : 10, "dexterity" : 10, "armor" : 10, "items" : {"helmet" : "VOID", "chest" : "VOID" , "weapon" : "VOID", "boots" : "VOID"}, "inventory" : [], "skills" : ["Punch"]}

#Variable globale utilisée en combat
myTurn = False

#Dictionnaire associant une image à un nom
images = {}

#Dictionnaire contenant les dialogues des différents pnjs
dialogs = {}

#Tableaux contenant les objets disponibles en boutique
shopItems = []

#Dictionnaire contenant les objets découverts dans les coffres.
chests = {}

#Variable indiquant la dernière fois qu'un mouvement a été effectué par le joueur - permet d'éviter les déplacements 'fusée'
lastMove = 0

#Variable permettant d'avoir un seul combat par case
canFight = True

def playMusic(path):
    pass

def nothing():
    pass

#Fonction de calcul pour le passage d'un niveau à un autre
def calcXP(lvl):
    return int( (900 / 99) * lvl * lvl + (9000 / 99) * lvl )

#Fonction permettant de verrouiller
def lock():
    global l
    l[0] = False

#Fonction permettant de déverrouiller
def unlock():
    global l
    l[0] = True

#Fonction permettant de tester si le joueur est verrouillé ou non
def isLocked():
    global l
    return l[0]

#Fonction appelée quand on appuie sur le bouton OK
def okMessage(callback):
    global txt, okButton
    txt.delete("all")
    okButton.destroy()
    callback() #On appelle la fonction passée en paramètre

#Fonction permettant d'afficher un message, et d'appeler une autre fonction quand on appuie sur OK
def message(string, callback):
    global txt, okButton
    txt.delete("all")
    txt.create_text(10, 10, anchor = NW, text = string)
    okButton = Button(txt, text = "OK", command = lambda : okMessage(callback))
    okButton.place(x = 30, y = 50)

#Fonction mettant à jour les infos de combat
def updateFightScreen():
    global stats, estats, main, hishp, myhp, mymp

    hishp.config(value = estats["HP"])

    myhp.config(value = stats["HP"])

    mymp.config(value = stats["MP"])

    main.itemconfig(main.getvar("ehp"), text = "HP : " + str(estats["HP"]) + " / " + str(estats["maxHP"]))

    main.itemconfig(main.getvar("hp"), text = "HP : " + str(stats["HP"]) + " / " + str(stats["maxHP"]))

    main.itemconfig(main.getvar("mp"), text = "MP : " + str(stats["MP"]) + " / " + str(stats["maxMP"]))

    main.update()


#Fonction pour faire des dégâts à l'ennemi
def dealDamage(amount):
    global stats, estats, main, menu, hishp
    amount = int(amount)
    amount -= estats["armor"]
    if amount < 0:
        amount = 0
    estats["HP"] -= amount
    a = main.create_text(64, 64, text = str(int(amount)) + " !", tag="to_delete")
    updateFightScreen()

#Fonction pour recevoir des dégâts
def takeDamage(amount):
    global stats, estats, main, txt, myhp
    amount = int(amount)
    amount -= stats["armor"]
    if amount < 0:
        amount = 0
    stats["HP"] -= amount
    main.create_text(448, 64, text = str(int(amount)) + " !", tag="to_delete")
    updateFightScreen()
    if stats["HP"] <= 0:
        print("Game OVER!") #TODO
        exit()

#TODO améliorer ça... Complètement fumé avec trop de différence
#Fonction testant l'esquive d'une attaque
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

#Fonction permettant d'alterner entre le tour de l'ennemi et du joueur
def changeTurn():
    global myTurn, menu, turnCounter, stats, estats
    turnCounter += 1

    temp = []
    etemp = []
    
    for effect in stats["effects"]:
        effect["TTL"] -= 1
        if effect["TTL"] == 0:
            temp.append(effect)
            for stat in list(effect.keys()):
                stats[stat] -= effect[stat]
                
    for effect in estats["effects"]:
        effect["TTL"] -= 1
        if effect ["TTL"] == 0:
            etemp.append(effect)
            for stat in list(effect.keys()):
                estats[stat] -= effect[stat]

    for t in temp:
        del(stats["effects"][t])
        
    for t in etemp:
        del(estats["effects"][t])

    if myTurn:
        myTurn = False
        enemyAttack()
    else:
        myTurn = True
        displaySkills()

#Fonction permettant de détruire tous les widgets du canvas txt
def clearTxt():
    global txt
    temp = []
    for key in txt.children.keys() :
        temp.append(txt.children[key])
    for child in temp:
        child.destroy()
        txt.update()

#Fonction permettant de détruire tous les widgets du canvas menu
def clearMenu():
    global menu
    temp = []
    for key in menu.children.keys() :
        temp.append(menu.children[key])
    for child in temp:
        child.destroy()
        menu.update()

#Fonction permettant de détruire tous les widgets du canvas main
def clearMain():
    global main
    temp = []
    for key in main.children.keys() :
        temp.append(main.children[key])
    for child in temp:
        child.destroy()
        main.update()

#Fonction permettant de faire attaquer l'ennemi
def enemyAttack():
    global menu, estats, stats, skills, txt
    chosenSkill = random.choice(estats["skills"])
    txt.create_text(15,15,anchor = NW, text = "L'ennemi utilise : " + chosenSkill)
    skills[chosenSkill]()
    time.sleep(2)
    txt.delete("all")
    main.delete("to_delete")
    changeTurn()

#Fonction de test de changement de niveau
def testLevelUp():
    global stats
    if stats["XP"] >= calcXP(stats["LVL"]):
        stats["XP"] -= calcXP(stats["LVL"])
        stats["LVL"] += 1
        stats["maxHP"] += 10
        stats["HP"] = stats["maxHP"]
        stats["maxMP"] += 10
        stats["MP"] = stats["maxMP"]
        stats["lvlPoints"] += 1
        message("LEVEL UP ! Niveau atteint : " + str(stats["LVL"]), testLevelUp)
    else:
        unlock()

#Fonction de gain d'expérience
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

#Fonction de test de gain d'objet à la fin du combat
def testLoot():
    global stats, estats
    pick = random.choice(estats["loot"])
    if pick != "VOID":
        inventoryAdd(pick)
        message("Vous trouvez : " + pick + " !", xp)
    else:
        xp()

#Fonction permettant d'utiliser un sort
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
        message("Vous Ãªtes victorieux !", testLoot)
        clearMain()
        showMenu()
        draw(xOffset,yOffset)
    else:
        changeTurn()

def strike():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(0.5 * stats["strength"] + 0.5 * stats["dexterity"])
    else:
        if dodgeTest():
            takeDamage(0.5 * estats["strength"] + 0.5 * estats["dexterity"])

def blub():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(0.2 * stats["HP"] + 1)
    else:
        if dodgeTest():
            takeDamage(0.2 * estats["HP"] + 1)

def slurp():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(0.2 * stats["strength"])
    else:
        if dodgeTest():
            takeDamage(0.2 * estats["strength"])

def bite():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(0.6 * stats["strength"] + 2)
    else:
        if dodgeTest():
            takeDamage(0.6 * estats["strength"] + 2)

def clawing():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(0.4 * stats["strength"] + 0.6 * stats["dexterity"])
    else:
        if dodgeTest():
            takeDamage(0.4 * estats["strength"] + 0.6 * estats["dexterity"])

def knife_throw():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(1.2 * stats["dexterity"])
    else:
        if dodgeTest():
            takeDamage(1.2 * estats["dexterity"])

def bone_throw():
    global myTurn, stats, estats
    if myTurn:
        if dodgeTest():
            dealDamage(1.2 * stats["dexterity"])
    else:
        if dodgeTest():
            takeDamage(1.2 * estats["dexterity"])

def warcry():
    global myTurn, stats, estats
    if myTurn:
        if stats["MP"] >= 15:
            stats["MP"] -= 15
            stats["effects"]["warcry"] = {"buff" : {"strength" : stats["LVL"]}, "TTL" : 5}
    else:
        estats["effects"]["warcry"] = {"buff" : {"strength" : estats["lvl"]}, "TTL" : 5}

#Dictionnaire des sorts
skills = {"Punch" : strike, "Blub" : blub, "Slurp": slurp, "Morsure" : bite, "Griffure" : clawing, "Lancer de couteau" : knife_throw, "Lancer d'os" : bone_throw}

#Dictionnaire de description des sorts
skillsDesc = {"Punch" : {"MP" : "0" , "desc" : "Un coup de poing basique."}, "Blub" : {"MP" : "0", "desc" : "BLBLBL"}, "Slurp" : {"MP" : "1", "desc" : "Sluuuuuurp"}, "Morsure" : {"MP" : "0", "desc":"Une simple morsure."}, "Lancer de couteau" : {"MP" : "0", "desc" : "Tout est dans le nom."}, "Lancer d'os" : {"MP" : "0", "desc" : "Etonnament, u nos lancé à grande vitesse fait très mal !"}}

#Fonction permettant le passage du menu titre au jeu
def titleToGame():
    global c
    c.destroy()
    unlock()

#Fonction d'affichage de la description d'un sort
def displayDesc(skill):
    global txt, skillsDesc
    txt.delete('all')
    txt.create_text(5,5, text = skill, anchor = NW)
    txt.create_text(5, 20, text = skillsDesc[skill]["MP"] + " MP", anchor = NW)
    txt.create_text(5, 35, text = skillsDesc[skill]["desc"], anchor = NW)

#Foonction d'affichage des sorts disponibles
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

#Fonction de chargement d'une sauvegarde avec pickle
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

#Fonction permettant de sauvegarder avec pickle
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

#Fonction permettant de retourner au jeu
def back():
    global txt
    txt.delete("all")
    clearTxt()
    showMenu()
    unlock()

#Fonction permettant d'attribuer un point dans une catégorie
def attribPoint(stat):
    global stats
    stats["lvlPoints"] -= 1
    stats[stat] += 1
    txt.delete("all")
    clearTxt()
    displayChar()

#Fonction pour afficher des infos à propos de l'état du joueur
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
    txt.create_text(15, 115, text = "Gold : " + str(stats["gold"]), anchor = NW)

    if stats["lvlPoints"] != 0:
        txt.create_text(150, 15, text = "Points à dépenser : " + str(stats["lvlPoints"]), anchor = NW)
        b = Button(txt, text = "+ Strength", command = lambda i = "strength" : attribPoint(i))
        b.place(x = 150, y = 35, height = 20, width = 64)
        b = Button(txt, text = "+ Widsom", command = lambda i = "wisdom" : attribPoint(i))
        b.place(x = 150, y = 55, height = 20, width = 64)
        b = Button(txt, text = "+ Dexterity", command = lambda i = "dexterity" : attribPoint(i))
        b.place(x = 150, y = 75, height = 20, width = 64)

    txt.create_text(270, 15, text = "LVL : " + str(stats["LVL"]), anchor = NW)

    exp = ttk.Progressbar(txt, orient = "horizontal", mode = "determinate", length = 50, maximum = calcXP(stats["LVL"]), value = stats["XP"], style = "green.Horizontal.TProgressbar")
    exp.place(x = 270, y = 35)

    txt.create_text(270, 55, text = "XP : " + str(stats["XP"]) + " / " + str(calcXP(stats["LVL"])), anchor = NW)

    hp = ttk.Progressbar(txt, orient = "horizontal", mode = "determinate", length = 100, maximum = stats["maxHP"], value = stats["HP"], style = "red.Horizontal.TProgressbar")
    hp.place(x = 400, y = 15, anchor = NW)

    txt.create_text(400, 35, text = "HP : " + str(stats["HP"]) + " / " + str(stats["maxHP"]), anchor = NW)

    mp = ttk.Progressbar(txt, orient = "horizontal", mode = "determinate", length = 100, maximum = stats["maxMP"], value = stats["MP"], style = "cyan.Horizontal.TProgressbar")
    mp.place(x = 400, y = 55, anchor = NW)

    txt.create_text(400, 75, text = "MP : " + str(stats["MP"]) + " / " + str(stats["maxMP"]), anchor = NW)

    b = Button(txt, text = "Retour", command = back)
    b.place(x = 550, y = 60, width = 108, height = 64)

#Fonction pour équiper un objet  depuis l'inventaire
def inventoryEquip(item): 
    global stats, itemIndex
    if stats["items"][itemIndex[item]["slot"]] != "VOID":
        unequip(stats["items"][itemIndex[item]["slot"]])
    equip(item)
    clearTxt()
    displayInventory()

#Fonction permettant de sortir du menu de l'inventaire
def invToMenu():
    global txt
    txt.delete("all")
    clearTxt()
    clearMenu()
    showMenu()
    unlock()

#Fonction appelée quand on choisit un objet dans l'inventaire
def pickItem(item):
    global itemIndex, slots, txt, caracs
    txt.delete("all")
    clearTxt()
    yo = 25
    if itemIndex[item]["slot"] in slots:
        b = Button(txt, text = "EQUIP", command = lambda i = item : inventoryEquip(i))
        b.place(x = 500, y = 50, width = 108, height = 64)
        for a in itemIndex[item]:
            if a in caracs:
                txt.create_text(10, yo, text = a + " : " + str(itemIndex[item][a]), anchor = NW)
                yo += 15
    txt.create_text(10, 115,anchor = NW, text = "Price : " + str(itemIndex[item]["price"]))
    yo = 10
    for t in itemIndex[item]["desc"]:
        txt.create_text(90, yo, text = t, anchor = NW)
        yo += 15

#Fonction permettant d'afficher l'inventaire
def displayInventory(offset = 0):
    global txt, menu, stats
    clearMenu()
    txt.delete("all")
    if len(stats["inventory"]) == 0:
        showMenu()
        return
    elif len(stats["inventory"]) < 5:
        lock()
        yo = 84
        for item in stats["inventory"].keys():
            b = Button(menu, text = item + " x " + str(stats["inventory"][item]), command = lambda i = item : pickItem(i))
            b.place(x = 10, y = yo, height = 64, width = 108)
            yo += 74
    else:
        lock()
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

#Fonction permettant de déséquiper un objet
def equipmentUnequip(item):
    global stats, itemIndex, txt
    stats["items"][itemIndex[item]["slot"]] = "VOID"
    inventoryAdd(item)
    clearMenu()
    txt.delete('all')
    clearTxt()
    displayEquipment()

#Fonction appelée quand on choisit un objet équipé
def pickEquipment(item):
    global itemIndex, stats
    yo = 10
    b = Button(txt, text = "UNEQUIP", command = lambda i = item : equipmentUnequip(i))
    b.place(x = 570, y = 60, width = 108, height = 64)
    for a in itemIndex[item]:
        if a in caracs:
            txt.create_text(10, yo, text = a + " : " + str(itemIndex[item][a]), anchor = NW)
            yo += 15
    yo = 10
    for t in itemIndex[item]["desc"]:
        txt.create_text(90, yo, text = t, anchor = NW)
        yo += 15

#Fonction permettant d'afficher l'équipement
def displayEquipment():
    global stats, menu
    lock()
    clearMenu()
    yo = 10
    for slot in list(stats["items"].keys()):
        if stats["items"][slot] == "VOID":
            b = Button(menu, text = slot + " :\nVIDE")
            b.place(x = 10, y = yo, width = 108, height = 64)
        else:
            b = Button(menu, text = slot + ":\n" + stats["items"][slot], command = lambda i = stats["items"][slot] : pickEquipment(i) )
            b.place(x = 10, y = yo, width = 108, height = 64)
        yo += 74
    q = Button(menu, text = "RETURN", command = invToMenu)
    q.place(x = 10, y = 306, width = 108, height = 64)

#Fonction permettant d'afficher le menu global
def showMenu():
    global menu
    c = Button(menu, text = "Perso", command = displayChar)
    c.place(x = 10, y = 10, width = 108, height = 64)
    i = Button(menu, text = "Inventaire", command = displayInventory)
    i.place(x = 10, y = 158, width = 108, height = 64)
    s = Button(menu, text = "Sauvegarder", command = save)
    s.place(x = 10, y = 232, width = 108, height = 64)
    e = Button(menu, text = "Equipement", command = displayEquipment)
    e.place(x = 10, y = 84, width = 108, height = 64)

#Fonction permettant d'afficher l'écran de combat
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

    a = main.create_text(10, 220, text = "HP : " + str(estats["HP"]) + " / " + str(estats["maxHP"]), anchor = NW, fill = "red")

    b = main.create_text(394, 260, text = "MP : " + str(stats["MP"]) + " / " + str(stats["maxMP"]), anchor = NW, fill = "blue")

    c = main.create_text(394, 220, text = "HP : " + str(stats["HP"]) + " / " + str(stats["maxHP"]), anchor = NW, fill = "red")

    main.setvar(name = "ehp", value = a)
    main.setvar(name = "mp", value = b)
    main.setvar(name = "hp", value = c)

    if random.random() * estats["dexterity"] <= stats["dexterity"]:
        myTurn = True
        message("Vous commencez !", displaySkills)
    else:
        myTurn = False
        message(name + " commence !", enemyAttack)

#Fonction permettant de lancer un combat
def fight(name):
    global main, txt, estats, menu, stats, turnCounter
    lock()
    turnCounter = 1
    main.delete("all")
    clearMenu()
    for key in enemyIndex[name].keys():
         estats[key] = enemyIndex[name][key]
    estats["effects"] = {}
    message("Combat contre un : " + name, lambda : fightScreen(name))

#Fonction permettant de lancer un dialogue avec un pnj
def pnjDialog(canvas, name):
    global dialogs
    if len(dialogs[name]) != 0:
        dialog(canvas, dialogs[name], unlock)
    else:
        unlock()

def openChest(coords, i):
    global chests, mapName, blocks, width, xOffset, yOffset
    txt.delete("all")
    clearTxt()
    if i < len(chests[coords]):
        item = chests[coords][i]
        inventoryAdd(item)
        message("Vous trouvez : " + item, lambda c = coords, i = i : openChest(c, i + 1))
    else:
        f = open(mapName + ".level", "r+")
        a = 0
        for i in range(9 + coords[1]):
            temp = f.readline()
            a += len(temp)
        f.seek(a + 3 * coords[0] + 9 + coords[1], 0) #Comportement étrange...
        f.write(str(OPEN_CHEST))
        f.close()
        blocks[coords[0] + coords[1] * width] = OPEN_CHEST
        draw(xOffset, yOffset)
        showMenu()
        unlock()

#Fonction permetttant d'intéragir avec des blocs
def blockAction(block):
  global stats, direction,x ,y
  if block == VOID_BLOCK:
    #playMusic('test.wav')
    message("LE CHAMPOMY C'EST POUR LES FAIBLES !", unlock)
  elif block == CHEST:
    lock()
    clearMenu()
    vx = 0
    vy = 0
    if direction == "Up":
        vy = -1
    elif direction == "Down":
        vy = 1
    elif direction == "Right":
        vx = 1
    elif direction == "Left":
        vx = -1
    openChest((x+vx,y+vy), 0)

#Fonction permettant de déclencher des triggers
def triggerAction(x , y, name):
  global width, blocks, pnjs, triggers, main, dialogs, enemyIndex, chests, canFight, xOffset, yOffset
  if name.startswith("FIGHT:"):
      if random.random() <= 1 / enemyIndex[name[len("FIGHT:"):]]["proba"] and canFight == True:
          canFight = False
          fight(name[len("FIGHT:"):])
  elif name.startswith("LOAD:"):
    canFight = False
    lock()
    blocks = []
    pnjs = []
    triggers = {}
    dialogs = {}
    chests = {}
    main.delete('all')
    clearMain()
    main.create_text(100,100,text = "Chargement...", fill = "white")
    main.update()
    loadResources(open(name[len("LOAD:"):],'r'))
    main.delete("all")
    draw(xOffset, yOffset)
    unlock()
  elif name.startswith("MESSAGE:"):
    lock()
    message(name[len("MESSAGE:"):], unlock)
  elif name.startswith("REGEN"):
    lock()
    message("Voyageur, bouffe AGNAGNAGN", regenMenu)
  elif name.startswith("SHOP:"):
    lock()
    clearMenu()
    shop(name[len("SHOP:"):])

#Fonction permettant de vendre des objets
def sell():
    global txt, menu, stats
    clearMenu()
    clearTxt()
    txt.delete("all")
    if len(stats["inventory"]) == 0:
        showMenu()
        unlock()
        return
    elif len(stats["inventory"]) < 5:
        yo = 84
        for item in stats["inventory"].keys():
            b = Button(menu, text = item + " x " + str(stats["inventory"][item]), command = lambda i = item : sellItem(i))
            b.bind("<Enter>", lambda e, i = item: itemDesc(i))
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
            b = Button(menu, text = list(stats["inventory"].keys())[i] + "x" + str(stats["inventory"][list(stats["inventory"].keys())[i]]), command = lambda i = list(stats["inventory"].keys())[i] : sellItem(i))
            b.bind("<Enter>", lambda e, i = item: itemDesc(i))
            b.place(x = 10, y = yo, width = 108, height = 64)
            yo += 74
    b = Button(menu, text = "RETURN", command = shopToMenu)
    b.place(x = 10, y = 10 + 6 * 74, width = 108, height = 64)

#Fonction d'affichage du menu de la boutique
def shop(shopFile):
    global txt, shopItems
    shopItems = []
    f = open(shopFile, 'r')
    for line in f:
        shopItems.append(line.rstrip("\n"))
    f.close()
    
    txt.create_text(10,10,anchor = NW, text = "La boutique. Vous pouvez acheter ou vendre des objets.")

    b = Button(txt, text = "ACHETER", command = buy)
    s = Button(txt, text = "VENDRE", command = sell)
    q = Button(txt, text = "RETURN", command = shopToMenu)
    b.place(x = 100, y = 50, width = 64, height = 64)
    s.place(x = 200, y = 50, width = 64, height = 64)
    q.place(x = 300, y = 50, width = 64, height = 64)

#Fonction permettant de passer de la boutique au menu global
def shopToMenu():
    global txt
    clearMenu()
    clearTxt()
    txt.delete("all")
    showMenu()
    unlock()

#Fonction permettant de vendre des objets
def sellItem(item):
    global stats, txt, itemIndex
    txt.delete("all")
    clearTxt()
    clearMenu()
    stats["gold"] += itemIndex[item]["price"]
    inventoryRemove(item)
    message("VENTE : " + item + " pour " + str(itemIndex[item]["price"]), sell)

#Fonction permettant d'acheter des objets
def buyItem(item):
    global stats, itemIndex, txt
    if stats["gold"] >= itemIndex[item]["price"]:
        stats["gold"] -= itemIndex[item]["price"]
        inventoryAdd(item)
        txt.delete("all")
        clearTxt()
        clearMenu()
        message("ACHAT : " + item, shopToMenu)
    else:
        return

#Fonction d'affichage du menu d'achat
def buy(offset = 0):
    global txt, shopItems, stats, itemIndex, skills
    clearMenu()
    clearTxt()
    txt.delete("all")
    if len(shopItems) < 5:
        yo = 84
        for item in shopItems:
            b = Button(menu, text = item + " : " + str(itemIndex[item]["price"]), command = lambda i = item : buyItem(i))
            b.bind("<Enter>", lambda e, i = item: itemDesc(i))
            b.place(x = 10, y = yo, height = 64, width = 108)
            yo += 74
    else:
        if offset + 4 > len(shopItems):
            offset -= 1
        elif offset < 0:
            offset = 0
        up = Button(menu, text = "UP", command = lambda o = offset - 1 : buy(offset = o))
        up.place(x = 10, y = 10, height = 64, width = 108)
        down = Button(menu, text = "DOWN", command = lambda o = offset + 1 : buy(offset = o))
        down.place(x = 10, y = 10 + 5 * 74, height = 64, width = 108)
        yo = 84
        for i in range(offset, offset + 4):
            b = Button(menu, text = shopItems[i] + " : " + str(itemIndex[shopItems[i]]["price"]), command = lambda i = shopItems[i] : buyItem(i))
            b.bind("<Enter>", lambda e, i = i: itemDesc(shopItems[i]))
            b.place(x = 10, y = yo, width = 108, height = 64)
            yo += 74
    b = Button(menu, text = "RETURN", command = shopToMenu)
    b.place(x = 10, y = 10 + 6 * 74, width = 108, height = 64)

#Fonction d'affichage de la description d'un objet
def itemDesc(item):
    global itemIndex, txt
    txt.delete("all")
    txt.create_text(15, 115, text = "Prix :" + str(itemIndex[item]["price"]), anchor = NW)
    yOffset = 10
    for line in itemIndex[item]["desc"]:
        txt.create_text(100, yOffset, anchor = NW, text=line)
        yOffset += 20
    if "strength" in itemIndex[item].keys():
        txt.create_text(15, 30, text = "Strength : " + str(itemIndex[item]["strength"]), anchor = NW)
    if "wisdom" in itemIndex[item].keys():
        txt.create_text(15, 50, text = "Wisdom : " + str(itemIndex[item]["widsom"]), anchor = NW)
    if "dexterity" in itemIndex[item].keys():
        txt.create_text(15, 70, text = "Dexterity : " + str(itemIndex[item]["dexterity"]), anchor = NW)
    if "armor" in itemIndex[item].keys():
        txt.create_text(15, 90, text = "Armor : " + str(itemIndex[item]["armor"]), anchor = NW)

#Fonction permettant de passer du menu de l'auberge au menu global
def regenToGame():
    global txt
    txt.delete("all")
    clearTxt()
    unlock()

#Fonction permettant de récupérer ses HP/MP
def regen():
    global stats, txt
    stats["HP"] = stats["maxHP"]
    stats["MP"] = stats["maxMP"]
    clearTxt()
    txt.delete("all")
    message("Vous vous sentez fais et dispo !", regenToGame)

#Fonction d'affichage du menu de l'auberge
def regenMenu():
    global menu,txt
    clearTxt()
    txt.create_text(10,10,anchor = NW, text = "Veux-tu te reposer pour 100 PO ?")
    yes = Button(txt, text="OUI", command = regen)
    no = Button(txt, text = "NON", command = regenToGame)
    yes.place(x = 100, y = 50,width = 40, height = 40)
    no.place(x = 150, y = 50,width = 40, height = 40)

#Fonction de chargement de la carte
def createMap(f):
  global width, height, blocks, pnjs, x, y, xOffset, yOffset, mapName, direction, images
  line = f.readline().rstrip("\n")
  mapName = f.readline().rstrip("\n")
  fbg = f.readline().rstrip("\n")
  images["fight_background"] = loadImage(fbg)
  width = int(f.readline().rstrip("\n"))
  height = int(f.readline().rstrip("\n"))
  x = int(f.readline().rstrip("\n"))
  y = int(f.readline().rstrip("\n"))
  direction = f.readline().rstrip("\n")
  images["player"] = images[direction]
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

#Fonction de chargement des pnjs
def createPNJ(f):
  global pnjs, width, images, dialogs
  line = f.readline().rstrip("\n") #{
  name = f.readline().rstrip("\n") #NOM
  ipath = f.readline().rstrip("\n") #Image
  path = f.readline().rstrip("\n")  #Dialogue
  x = int(f.readline().rstrip("\n")) #X
  y = int(f.readline().rstrip("\n")) #Y
  pnjs[x + y * width] = name
  images[name] = loadImage(ipath)
  file = open(path, "r")
  dialogs[name] = file.readlines()
  file.close()
  line = f.readline().rstrip("\n") #}

#Fonction de chargement des triggers
def createTrigger(f):
  global triggers, width
  line = f.readline().rstrip("\n")
  name = f.readline().rstrip("\n")
  x = f.readline().rstrip("\n")
  y = f.readline().rstrip("\n")

  try :
      x = int(x)
      y = int(y)
      triggers[x + y * width].append(name)

  except Exception :
      i = x.find("-")
      startX = int(x[:i])
      endX = int(x[i + 1:])

      i = y.find("-")
      startY = int(y[:i])
      endY = int(y[i + 1:])

      for a in range(startX, endX + 1):
          for b in range(startY, endY + 1):
              triggers[a + b * width].append(name)

  line = f.readline().rstrip("\n")

#Fonction permettant de charger des objets
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

#Fonction de chargement des ennemis
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

def loadChest(f):
    global chests
    line = f.readline().rstrip("\n") # {
    x = int(f.readline().rstrip("\n")) # X
    y = int(f.readline().rstrip("\n")) # Y
    chests[(x,y)] = []
    line = f.readline().rstrip("\n")
    while line != "}":
        chests[(x,y)].append(line)
        line = f.readline().rstrip("\n")

#Fonction de chargement globale
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
  elif line == "[CHEST]":
    loadChest(f)
  if line != '':
    loadResources(f)
  for block in blocks:
    images[block] = loadImage(blockIndex[block])

#Fonction d'ajout d'un objet à l'inventaire du joueur
def inventoryAdd(name):
    global stats
    if name in stats["inventory"].keys():
        stats["inventory"][name] += 1
    else:
        stats["inventory"][name] = 1

#Fonction de retrait d'un objet de l'inventaire
def inventoryRemove(name):
    global stats
    stats["inventory"][name] -= 1
    if stats["inventory"][name] == 0:
        stats["inventory"].pop(name, None)

#Fonction de vérification
def check():
    global stats
    if stats["HP"] > stats["maxHP"]:
        stats["HP"] = stats["maxHP"]
    if stats["MP"] > stats["maxMP"]:
        stats["MP"] = stats["maxMP"]

#Fonction permettant d'équiper un objet de l'inventaire
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

#Fonction permettant de déséquiper un objet
def unequip(name):
    global stats, itemIndex, caracs
    if name in stats["items"].values():
        stats["items"][itemIndex[name]["slot"]] = "VOID"
        inventoryAdd(name)
        for key in itemIndex[name].keys():
            if key in caracs:
                stats[key] -= itemIndex[name][key]
        check()

#Fonction traitant les entrées clavier
def keyListener(event):
  global LEFT, RIGHT, UP, DOWN, ENTER,blocksWidth, blocksHeight, x , y, direction, width, height, blocks, pnjs, triggers, xOffset, yOffset, txt, lastMove, canFight
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
      canFight = True
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

#Début du programme principal
createWindow(keyListener)

images["Background"] = loadImage("background.png")

images["Up"] = loadImage("up.png")
images["Down"] = loadImage("down.png")
images["Left"] = loadImage("left.png")
images["Right"] = loadImage("right.png")

images["fight_image"] = loadImage("gentil.png")

images[OPEN_CHEST] = loadImage("OPEN_CHEST.png")

main, txt, menu = gameCanvas()

showMenu()

c = titleMenu(titleToGame, images["Background"])

#Fonction de dessin de la map, du joueur, et de tout le reste
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

f = open('mobs.txt','r')
loadResources(f)
f.close()

if os.path.exists("test.save"):
    load()
else:
    stats = {"LVL" : 1, "XP" : 0,"effects" : {} ,"lvlPoints" : 0, "gold" : 0, "maxHP" : 20, "HP" : 20, "maxMP" : 100, "MP" : 100, "strength" : 10, "wisdom" : 10, "dexterity" : 10, "armor" : 0, "items" : {"helmet" : "VOID", "chest" : "VOID" , "weapon" : "VOID", "boots" : "VOID"}, "inventory" : [], "skills" : ["Punch"]}
    f = open('level1.level','r')
    loadResources(f)
    f.close()

draw(xOffset, yOffset)

runWindow()
