from tkinter import *
from tkinter import ttk
import tkinter.font
from PIL import Image, ImageTk

def loadImage(path):
    img = Image.open(path)
    img2 = ImageTk.PhotoImage(img)
    return img2

def createWindow(keyListener):
    global root, windowWidth, windowHeight
    root = Tk()

    windowWidth = 704
    windowHeight = 704

    root.title("AVENTURE")  #TITRE
    root.resizable(width = FALSE, height = FALSE) #Pas redimensionnable
    root.geometry(str(windowWidth)+ "x" + str(windowHeight)) #On choisit les dimensions de la fenetre
    root.bind("<Key>",keyListener) #On ajoute le keyListener

    default_font = tkinter.font.nametofont("TkDefaultFont") #Mise en place du font
    default_font.configure(family="Breathe Fire", size = 14) #Breathe Fire

def gameCanvas():
    global windowWidth, windowHeight, root
    mainCanvas = Canvas(root, width = 576 ,height = 576, bg = "black", bd = 0, highlightthickness=0)
    textCanvas = Canvas(root, width = 704,height = 128, bg = "#4d4dff", bd = 0, highlightthickness=0)
    menuCanvas = Canvas(root, width = 128,height = 576, bg = "#9999ff", bd = 0, highlightthickness=0)

    mainCanvas.place(x = 0, y = 0)
    textCanvas.place(x = 0, y = 576)
    menuCanvas.place(x = 576, y = 0)

    

    root.update()

    return mainCanvas, textCanvas, menuCanvas

def titleMenu(onPlay, background):
    global root, windowWidth, windowHeight
    c = Canvas(root,width = 704, height = 704)
    c.place(x = 0, y = 0)

    c.create_image(0, 0, anchor = NW, image = background)

    playButton = Button(c, text="PLAY",command = onPlay)
    quitButton = Button(c, text="EXIT",command = root.destroy)

    #TODO des images

    playButton.place(x = 250, y = 250)
    quitButton.place(x = 250, y = 350)

    return c

def dialogNext():
    global label, d, index, root, b, l
    index += 1
    if index < len(d):
        label.config(text = d[index], bg = "#4d4dff")
        root.update()
    else:
        label.destroy()
        b.destroy()
        root.update()
        l()

def dialog(canvas, dialog, unlock):
    global label, d, index, b, l
    l = unlock
    index = 0
    d = dialog
    label = Label(canvas, text = d[index], bg = "#4d4dff")
    label.place(x = 30, y = 35)
    button = Button(canvas, text = "OK", command = dialogNext)
    button.place(x = 30, y = 60)
    b = button
    root.update()

def okbutton():
    global entry
    print(entry.get())
    entry.delete(0,'end')

def questionnaire(canvas):
    global entry, root
    entry = Entry(canvas)
    button = Button(canvas, text = "OK", command = okbutton)
    entry.place(x = 50, y = 50)
    button.place(x = 50, y = 100)

def runWindow():
    root.mainloop()

def destroy():
    root.destroy()

