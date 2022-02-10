import threading
from tkinter import ttk
import time
import copy
import tkinter


import matplotlib as mlp
import matplotlib.pyplot as plt

from keras_visualizer import visualizer 
from tkinter import *


#GUIMain Klasse macht halt die GUI

instance = None

class GuiMain(threading.Thread):
    
    MainOb = None                   #Verweiß auf das Main Objekt

    root = None                     #Tkinter Window 
    c = None                        #GameField Canvas
    nesC = None                     #DrawCanvas für den NES Controller
    text = None                     #TextArea

    backgroundColor = "green"       #BackgroundGameFieldFarbe
    CellColor = "red"               #ForegroundGameFieldFarbe
    cellSize = 25                   #große der Cells

    LastLastGameField = []          #LastLastVersion of the GameField
    frame = 0                       #last Frame Dauer

    wantGUI = False

#   init/Konst
#
#   Aufgabe:
#   startet den Thread und speichert die Main Ref
    def __init__(self, main):
        global instance
        instance = self
        self.MainOb = main
        threading.Thread.__init__(self)
        self.start()

#    run
#
#    Aufgabe:
#    wird von der Thread klasse geerbt und ist die Methode die im neuen Thread ausgeführt wird
#    Die Methode hat eine while Schleife die so lange läuft, bist sie die Var ProgrammRunnning false ist
#    Solage dem nicht so ist wird die GUI Frame Methode aufgerufen.
#    Außerdem wird hier das GUI erstellt

    def run(self):
        self.root = Tk(className='TetrisAI')
        self.setupGui()
        self.LastLastGameField = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.renderImage()
        


        while(self.MainOb.ProgrammRunning ):
            try:
                self.GuiFrame()
            except tkinter.TclError:
                self.MainOb.ProgrammRunning = False
            except tkinter.TclError:
                self.MainOb.ProgrammRunning = False




#    Setup GUI
#
#    Aufgabe:
#    Erstellt das Tkinter Window und added alle widgets(ink plazieren)

    def setupGui(self):
        root = self.root
        root.geometry("700x550")
        root.resizable(False, False)
        self.c = Canvas(root, bg=self.backgroundColor,
                        height=self.cellSize*20, width=self.cellSize*10)
        self.c.place(relx=0.21, rely=0.5, anchor='center')
        self.text = Text(self.root, height=10, width=47)
        self.text.pack()
        self.text.place(relx=.69, rely=0.2, anchor='center')

        y1 = 0.36

        self.save = Button(self.root,height=3,width=13,text="Save", command=save)
        self.save.pack()
        self.save.place(relx=.422,rely=y1, anchor="nw")

        self.load = Button(self.root,height=3,width=13,text="Load", command=load)
        self.load.pack()
        self.load.place(relx=.602,rely=y1, anchor="nw")

        self.prog = Button(self.root,height=3,width=13,text="Show Progress",command=showProgress)
        self.prog.pack()
        self.prog.place(relx=.782,rely=y1, anchor="nw")
        
        self.toogleGUI = Button(self.root,height=3,width=13,text="Toogle GUI", command=toogleUI)
        self.toogleGUI.pack()
        self.toogleGUI.place(relx=.422,rely=0.48, anchor="nw")

        self.visualize1 = Button(self.root,height=3,width=13,text="Visualize", command=visualize)
        self.visualize1.pack()
        self.visualize1.place(relx=.602,rely=0.48, anchor="nw")


        self.nesC = Canvas(root, bg="light grey", height=200, width=375)
        self.nesC.place(relx=0.69, rely=0.775, anchor='center')
        self.initDraw()

#    RenderImage
#
#    Aufgabe:
#    Rendert das GameField bzw. das Letzte was angekommen ist

    def renderImage(self):
        if(self.wantGUI):
            cellSize = self.cellSize
            for k, x in enumerate(self.MainOb.LastGameField):
                for i, y in enumerate(x):
                    if(self.LastLastGameField[k][i] != y):
                        self.c.create_rectangle(i*cellSize, k*cellSize, i*cellSize+cellSize, k*cellSize+cellSize,
                                                fill=self.CellColor if y == 1 else self.backgroundColor,width=1)
            self.renderInputCon()
            
        self.LastLastGameField = copy.deepcopy(self.MainOb.LastGameField)


#    renderInputConqaqwwwwwww
#
#    Aufgabe:
#    Zeichnet die Input Buttons des NES Controllers in der GUI bezieht sich auf die letzte eingabe die in der Main gespeichert ist

    def renderInputCon(self):
        abstand = 5
        colorTrue = "red"
        colorFalse = "white"

        Inputs = self.MainOb.LastInput

        #L
        self.drawRect(50-abstand, 80, 40, 40,
                      color=colorTrue if(Inputs == 0)else colorFalse)
        #R
        self.drawRect(130+abstand, 80, 40, 40,
                      color=colorTrue if(Inputs == 1)else colorFalse)
        #D
        self.drawRect(90, 120+abstand, 40, 40,
                      color=colorTrue if(Inputs == 2)else colorFalse)
        self.drawRect(90, 40-abstand, 40, 40)

        self.drawRect(375-80-5, 80, 40, 40)
        #A
        self.drawRect(375-140-5, 80, 40, 40,
                      color=colorTrue if(Inputs == 3)else colorFalse)

        pass


#    initDraw
#    Aufgabe:
#    macht so den Initialize Draw ist ein bisschen überflüssig, aber YOLO
 
    def initDraw(self):
        self.nesC.create_rectangle(375, 200, 4, 4, outline="black", width=2)

        abstand = 5

        self.drawRect(50-abstand, 80, 40, 40)
        self.drawRect(130+abstand, 80, 40, 40)
        self.drawRect(90, 120+abstand, 40, 40)
        self.drawRect(90, 40-abstand, 40, 40)

        self.drawRect(375-80-5, 80, 40, 40)
        self.drawRect(375-140-5, 80, 40, 40)


#    DrawRect
#    Aufgabe:
#    Macht das zeinen von Rechtecken einfacher

    def drawRect(self, x, y, width, height, color="white"):
        self.nesC.create_rectangle(
            x, y, x+width, y+height, outline="black", width=1, fill=color)


#    GUIFrame
#
#    Aufgabe: 
#    Macht alles was in einem Frame in der Gui so zu tun ist, ja lol ey was ein Wunder.  
#    Um genau zu seint wird die Zeit des Frames gemessen der Text für die Text Area gesetzt.
#    Das GameField gerendert und den 0 8 15 stuff halt. Input wird auch gezeichnet

    def GuiFrame(self):
        start = time.time()

        if self.wantGUI:
            self.renderImage()
            str1 = self.getText()
            self.text.delete(1.0, "end")
            self.text.insert(1.0, str1)
            end = time.time()
            self.frame = end - start

        #self.root.update_idletasks()
        self.root.update()


#    Get Text Methode:
#
#    Aufgabe:
#    berechnet den Anzuzeigenden Text, der in der GUI in der Text Area gezeigt wird.
#    
#    Return: String mit allen Infos

    def getText(self):
        str1 = "Frame Length: "+str(self.frame)
        str1 += "\n"+self.MainOb.GetSocketTimeStuff()
        str1 += "\nStatus: "+self.MainOb.Status
        str1 += "\nConnected: "+str(self.MainOb.IsConnected)
        str1 += "\nLastScore:"+str(self.MainOb.LastScore)
        str1 += "\nLastNextBlock:"+str(self.MainOb.LastNextBlock)
        str1 += "\nStep: "+ str(self.MainOb.currentStep)

        return str1

 ##TODO: Edge weg machen beim GameField
 ##TODO: SaveAI Button


def save():
    print("save")
    instance.MainOb.KIMain.save = True

def load():
    print("load")
    instance.MainOb.KIMain.load = True


def showProgress():
    try:
        plt.ylabel = "Rot=Score   Blau=Reward"
        Episoden = instance.MainOb.KIMain.Episoden
        
        plotarr1 = []
        plotarr2 = []
        #indexe = []

        i = 0
        for x in Episoden:
            if(x.Score != 0):
                plotarr1.append(x.Score)
            plotarr2.append(x.Reward)
            #indexe.append[i]
            i+=1

        plt.plot(plotarr2,"b-")
        plt.plot(plotarr1,"r-")
        plt.grid(True)
        plt.show()
    except:
        print("sollte jetzt angezeigt werden, wenn nicht schau in der Zeile 277GuiMain")

def toogleUI():
    instance.wantGUI = not instance.wantGUI
    print("Toggle UI")

def visualize():
    visualizer(instance.MainOb.KIMain.model, format='png', view=True)