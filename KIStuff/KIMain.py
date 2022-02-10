


import imp
import random
from time import time
from tkinter.constants import SE
from rl import agents
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D
from tensorflow.keras.optimizers import Adam;

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy

import time

import numpy as np

import keras.backend as K


from KIStuff.Envioment import TetrisEnv
from Main import Main

#   KIMain Klasse
#   Aufgabe:
#   Managed den ganzen KI Stuff
class KIMain():

    Episoden = []
    LReward = 0

    def __init__(self,Main):
        self.Main = Main
        self.env = TetrisEnv(Main)
        self.score = 0
        height, width, channels = self.env.observation_space.shape
        model = self.setupDLM(height= height,width = width,channels = channels,actions = 5)
        self.model = model
        self.agent = self.setupAgent(model1=model,actions=self.env.action_space.n)
        self.agent.compile(Adam(learning_rate=1e-2))

    def doGameStuff(self):
        if(self.save):
            self.save1()

        if(self.load):
            self.load1()

        self.agent.fit(self.env,nb_steps=2000000,visualize=True,verbose=25000)
        #print("Lreward: "+str(self.LReward))
        self.save1(str(time.time()))
       
        self.env.reset()
        #print("doStuffEinmalFertig")



    def setupDLM(self,height, width,channels, actions):
            model = Sequential()
            model.add(Convolution2D(32,(1,1),activation="relu",input_shape=(1,height,width,1)))
            model.add(Convolution2D(64,(1,1),activation="relu"))
            model.add(Convolution2D(64,(1,1),activation="relu"))
            model.add(Flatten())
            model.add(Dense(512, activation="relu"))
            model.add(Dense(256, activation="relu"))
            model.add(Dense(5,activation="linear"))
            model.summary()
            return model

    save = False
    load = False

    def save1(self,speicherort = ""):
        path = "models/"+speicherort+"/TetrisAIModel01.h5f"

        self.agent.save_weights(path)
        self.save = False
        string = ""
        for e in self.Episoden:
            string+=str(e.Score)+";"+str(e.Reward)+"\n"
        with open("models/Episodes.txt", "w") as text_file:
            text_file.write(string)
        print("saved11111")

    def load1(self):
        self.Episoden = []

        self.agent.load_weights(self.path)
        self.load = False

        f = open("models/Episodes.txt","r")
        lines = f.readlines()
        for line in lines:
            if(line != ""):
                splited = line.split(";")
                score = int(splited[0])
                reward1 = float(splited[1])
                ep = Episode(score,reward1)
                self.Episoden.append(ep)
        


    def setupAgent(self,model1,actions):
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(),attr="eps",value_max=1.,value_min=.1, value_test=.2,nb_steps=5000)
        memory = SequentialMemory(limit=1000,window_length = 1)
        dqn = DQNAgent(model =model1,memory=memory,policy=policy,enable_dueling_network=True, dueling_type="avg",nb_actions = actions,nb_steps_warmup = 100)
        return dqn

#   CalcMove
#   Aufgabe:
#   Fragt die KI was zu tun ist
#   Parameter:  GameField 2D Array mit 0 und 1 je nach dem
#   Return:     Array mit den zu erledigenden Moves
    def CalcMove(self, GF, NextBlock):
        action = [random.choice([0,1]),random.choice([0,1]),random.choice([0,1]),random.choice([0,1])]
        n_state, reward, done, info = self.env.step(action)
        self.score+=reward
        print("NEIN DIGGI")
        print(self.score)
        return action

    def Reset(self):
        self.score = 0

#   trainKI
#   Aufgabe:
#   Trained die AI für den nächsten durchlauf
    def TrainKI(self, score):
        pass


print("herre")


# TODO calcMove gescheit machen

class Episode():
    def __init__(self,Score,Reward):
        self.Score = Score
        self.Reward = Reward