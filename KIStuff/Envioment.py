from gym import Env
from gym.spaces import  Discrete, Box
import numpy as np
import copy
import Main


class TetrisEnv(Env):
    def __init__(self, Main):
        self.socket = None
        self.Main = Main
        self.action_space = Discrete(5)
        self.observation_space = Box(shape=(21,10,1),low = 0, high=1)
        self.state = emptyState()
        self.steps = 0
        self.LastStep = 0

    lastReset = None

    def step(self,action): 
        socket = self.Main.getInfo()
        self.socket = socket
        self.Main.LastInput = action
        reset = self.Main.shouldReset()
        if(reset == 1):
            #print("sendToReset")
            pass
        h = howManyHoles(self.state)-4
        if(h > 0):
            reset = 1
        self.Main.GameFieldReader.sendInfo(socket,int(action == 0),int(action == 1),int(action == 2),int(action == 3),reset)
        if(reset == 1):
            self.Main.SetupConnection()
       

        self.state = self.Main.getLastState()
        diffScore = self.Main.LScore - self.Main.LLScore

        info = {}

        self.Main.LLScore = self.Main.LScore
        self.Main.LLNextBlock = self.Main.LastNextBlock


        self.Main.LLGameField = copy.deepcopy(self.Main.LastGameField)

        epFertig = 0

        if(self.lastReset != None and self.lastReset != reset):
            epFertig = reset

        self.lastReset = reset

        bool1 = (epFertig == 2 or epFertig == 1)
        self.steps += 1
        reward = 0
        if(bool1):
            if(self.steps< 2):
                bool1 = False
                
            else:
                reward, holes = calcReward(self.state,self.steps,self.LastStep)
                self.steps = 0
                if self.steps > self.LastStep:
                    self.LastStep = self.steps

        if(reset == 1):
            self.Main.KIMain.Episoden.append(Episode(self.Main.LScore,self.Main.KIMain.LReward))
            self.Main.KIMain.LReward = 0

        self.Main.KIMain.LReward = self.Main.KIMain.LReward + reward
        return self.state,reward,bool1 , info

    def render(self,mode = "human"):
        pass

    def reset(self):
        self.state = emptyState()
        self.observation_space = Box(shape=(21,10),low = 0, high=1)
        self.Main.KIMain.Reset()
        self.Main.Reset() 
        return self.state

def emptyState():
    ar = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ]
    return Main.createState(ar,-1)

#brauche noch State in Main
#brauche noch dieses a synchrone zeugs

def calcReward(State,Steps, LastSteps):
    reward = 0
    #HowManyHoles = howManyHoles(State)-4
    StepsDiff = Steps-LastSteps
    if(not StepsInRange(Steps,LastSteps,10)):
        reward = -StepsDiff
    else:
        if(StepsDiff > 0):
            reward = StepsDiff
        else:
            reward = .1

    return (reward*20,-1)


def StepsInRange(Steps, LastSteps, Tollerenz):
    Toll = LastSteps*(Tollerenz/100)
    return(Steps > LastSteps-Toll)

def howManyHoles(State):
    height = 21
    width = 10
    loecher = 0
    for i in range(1,height):
        for j in range(0,width):
            IsValidStartPoint = (State[i][j] == 1 or i == 20)

            if(IsValidStartPoint):
                n = 1
                while(State[i-n,j]==0 and i-n >= 0):
                    n+=1
                if(n > 1):
                    loecher+=1
    return loecher-10

class Episode():
    def __init__(self,Score,Reward):
        self.Score = Score
        self.Reward = Reward