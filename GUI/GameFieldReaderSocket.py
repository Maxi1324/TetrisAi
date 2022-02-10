import socket
import time

#   loadStuff Klasse
#   Aufgabe:
#   Stellt die Verbindung zum Emulator her


class loadStuff:

    sec = -1  # Sekunden Offset
    sec2 = 0  # Aktuelle Sekunde
    count = 0  # PackageCount
    strNa = ""  # Sring der die Anzahl der Packages in der Sekunde angibt
    host = None  # Adresse für initSocket
    port = None  # port für initSocket

    s = None  # Eingehnder Socet
    conn = None  # Socket über den auf den Emulator zugegriffen werden


#   init draw/ konstruktor
#   Aufgabe:
#   macht so Konstrucor stuff


    def __init__(self, host, port):
        self.host = host
        self.port = port


#   TimeStuff
#   Aufgabe:
#   sorgt für das Speichern der in Packages pro Sekunde
#   returned nichts speichert in strNa

    def timeStuff(self):
        s1 = int(time.time())
        if(self.sec == -1):
            self.sec = s1

        if(self.sec2 == s1):
            self.count = self.count + 1
        else:
            # print("second: "+str(self.sec2-self.sec)+" packets: "+str(self.count))
            self.strNa = "second: " + \
                str(self.sec2-self.sec)+" packets: "+str(self.count)
            self.sec2 = s1
            self.count = 0


#   initSocket
#   Aufgabe:
#   Stellt Socket zu verfügung
#   Return Socket zum Emulator

    def initSocket(self):
        if(self.s == None):
            s = socket.socket()
            s.bind((self.host, self.port))
            s.listen()
            self.s = s
        conn, addr = self.s.accept()
        self.conn = conn
        return conn


#   #waitForConnection
#   Aufgabe:
#   warten so lange bis eine connection da ist
#   Parameter:  socket auf dem gewartet werden soll


    def waitForConnection(self, socket):
        while (socket.recv(1024).decode() != "start"):
            pass
        socket.send("start".encode())


#   GetInfo
#   Aufgabe:
#   holt mit hilfe des Sockets information
#   Parameter:  socket über den recv werden soll
#               2D Array in das die Info rein gejizzed werden sollen
#   Return:     NextBlock

    def getInfo(self, socket, GameField):
        try:
            self.timeStuff()
            text = socket.recv(1024).decode()
            parts = text.split(":")
            GameFieldPart = parts[0]
            NextBlock = round(float(parts[1]), 1)
            for i in range(0, len(GameFieldPart)):
                posY = i//10
                posX = i-(10*posY)
                GameField[posY][posX] = int(GameFieldPart[i])
            return (NextBlock,self.convertScore(parts[2]))
        except:
            return (0,0)


#   getScore
#   Aufgabe:
#   resives den Score
#   Parameter:  Socket
#   Return:     Score

    def getScore(self,socket):
        text = socket.recv(1024).decode()
        if(text == ""):
            print("score ist falsch")
            return 0
        parts = text.split(";")
        r = 0
        for i in range(0,3):
            part1 = parts[i]
            mult = pow(16,i*2)
            zahl = int(part1)*mult
            r = r +  zahl

        return int(str(hex(r)).split("x")[1])

    def convertScore(self,text):
        if(text == ""):
            print("score ist falsch")
            return 0
        parts = text.split(";")
        r = 0
        for i in range(0,3):
            part1 = parts[i]
            mult = pow(16,i*2)
            zahl = int(part1)*mult
            r = r +  zahl

        return int(str(hex(r)).split("x")[1])


#   sendInfo
#   Aufgabe:
#   Sendet Informationen an den Emulator
#   Parameter:  Socket über den gesendet wird   Socket
#               A, D, L , R Buttons             bools
#               Soll resetten                   bool

    def sendInfo(self, Socket, A, D, L, R, Reset):
        str1 = (str(int(A))+str(int(D))+str(int(L)) +
                str(int(R))+str(int(Reset))).encode()
        Socket.send(str1)

# 0 AButton
# 1 DownButton
# 2 LeftButton
# 3 RightButton
# 4 Reset