import time

import numpy as np
from tensorflow.python.keras.backend import shape
import GUI.GuiMain
import KIStuff.KIMain
import GUI.GameFieldReaderSocket
import threading
import copy

#Main
#Aufgabe:
#Alles Managen

class Main():

    host = '127.0.0.1'              #localHostAdresse für den Socket
    port = 55535                    #zu Öffnender Port für den Socket

    LastGameField = [               #Letztes erhaltende GameField
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
    LLGameField = []

    LastNextBlock = None            #speichert den letzten erhaltenen NextBlock        
    LastScore = None                #letzter erhaltener Score           
    LastInput=4                  #Letzter Input
    Status = ""                     #Status
    LScore = 0
    LLScore = 0
    LLNextBlock = 0

    isTraining = True               #gibt das Abruchs kriteruim an. Wenn es Trainiert wird das Spiel nicht zu 100% gespielt sondern nur für eine bestimmte Zeit
    TrainDur = 60                    #Zeigt an wie lange ein Training run läuft

    GameFieldReader = None          #Ref zum SocketGameFieldReader ob
    GuiMain = None                  #Ref zum GuiMain Ob
    socket = None                   #Ref zum ConnSocket
    KIMain = None                   #Ref zum KIMain Ob

    ProgrammRunning = True          #Zeigt an, ob das Programm laufen soll, oder beendet
    IsConnected = False             #Zeigt den verbindungs Status zum Emulator an

    lastReset = start = time.time() #Speichert wann der Letzte Reset des GameFields gemacht wurde

    currentStep = 0


#   init
#   Aufgabe:
#   erstellt alle Objekte und startet den Update Loop

    def __init__(self):
        self.LLGameField = copy.deepcopy(self.LastGameField)
        print("hallo")
        self.Status = "Creating Instaces"
        self.GameFieldReader = GUI.GameFieldReaderSocket.loadStuff(self.host, self.port)
        #self.GuiMain = GUI.GuiMain.GuiMain(self)
        self.Status = "Starting MainLoop"
        self.KIMain = KIStuff.KIMain.KIMain(self)
        #self.KIMain.load1()
        self.SetupConnection()

        while(True):
            self.KIMain.doGameStuff()



#   Update
#   Aufgabe: 
#   Managen was passiert

    def Update(self):
        if (self.IsConnected):
            self.Status = "ResAndProcessing information"
            self.SendGetInformation()
        else:
            self.Status = "trying to connect to Emulator"
            self.SetupConnection()


#   SendGetInformation
#   Aufgabe:
#   Wird von der Update Methode aufgerufen und Updated das GameField ruft die ProcessInformation Methode auf und sendet die Inputs an den Emulator
        
    def SendGetInformation(self):
        socket = self.GameFieldReader.initSocket()
        self.LastNextBlock, score = self.GameFieldReader.getInfo(socket,self.LastGameField)
        self.LScore = score
        input1 = self.ProcessInformation()
        self.LastInput = input1
        self.GameFieldReader.sendInfo(socket,input1[0],input1[1],input1[2],input1[3],input1[4])
        self.LLScore = self.LScore
        self.LLNextBlock = self.LastNextBlock
        if(input1[4] == 1):
            self.LastScore = self.GameFieldReader.getScore(socket)
            self.Reset()

    def getInfo(self):
        socket = self.GameFieldReader.initSocket()
        self.LastNextBlock, score = self.GameFieldReader.getInfo(socket,self.LastGameField)
        self.LScore = score
        return socket

#   ProcessInformation
#   Aufgabe: Rechnet den nächsten Input aus außerdem schaut ob reset nötig

    def ProcessInformation(self):
        sr = self.shouldReset()
        if(sr == 1):
            self.Reset()

        result = self.KIMain.CalcMove(self.LastGameField,self.LastNextBlock)
        result.append(sr)
        return result


#   SetupConnection
#   Aufgabe:
#   Stellt die Verbindung mit dem Emulator auf

    def SetupConnection(self):
        socket = self.GameFieldReader.initSocket()
        self.GameFieldReader.waitForConnection(socket)
        self.IsConnected = True
        self.lastReset = time.time()


#   shouldReset
#   Aufgabe:
#   Überprüft ob das Spiel gereseted werden soll
#   Return:     int 1 Ja 0 Nein

    def shouldReset(self):
        #if(self.currentStep == 4999):
         #   self.currentStep = 0
         #   print("lastStep")
         #   return 1
        self.currentStep = self.currentStep+1
        if(self.isTraining):
            cellIsFree = False
            for k, x in enumerate(self.LastGameField):
                for i, y in enumerate(x):
                    if(y== 0):
                        cellIsFree = True
            if(not cellIsFree):
                print("spiel Verloren")
                return 1
                
        return 0


#   Reset
#   Aufgabe:
#   Reset beendet den Trainings lauf und setzt alles auf Anfang
    def Reset(self):
        self.IsConnected = False
        self.lastReset = time.time()
        self.KIMain.TrainKI(self.LastScore)


#   GetSocketTimeSuff
#   Aufgabe:  
#   Stellt die strNA Variable vom GameField Reader zur verfügung

    def GetSocketTimeStuff(self):
        return self.GameFieldReader.strNa

    def getLastState(self):
        return createState(self.LLGameField,self.LLNextBlock)

    def getState(self):
        return createState(self.LastGameField, self.LastNextBlock)


def createState(GameField, NextBlock):
    npArray = np.array(GameField.copy())

    original = round((NextBlock)/(1/7))

    for i in range(0,10):
        npArray= np.append(npArray,0 if original != i else 1)

    npArray= np.reshape(npArray,[21,10,1])

    return npArray



#   Main Methode
#   Aufgabe:
#   Initiert das Ganze Programm

if __name__ == '__main__':
    m = Main()
    m.ProgrammRunning = False

#TODO KIEnde
