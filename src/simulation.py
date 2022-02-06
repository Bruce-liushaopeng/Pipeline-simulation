from timeGenerator import TimeGenerator
import numpy as np
from random import seed, random
class simulation():
    def __init__(self):
        self.part1Target = 10
        self.p2Target = 10
        self.p3Target = 10
        self.p1Made = 0
        self.p2Made = 0
        self.p3Made = 0
        self._clock = 0.0
        self.bufferCapacity = 2
        self.bufferC1W1 = 0
        self.bufferC1W2 = 0
        self.bufferC2W2 = 0
        self.bufferC1W3 = 0
        self.bufferC3W3 = 0
    def sim(self):
        timeGenerator = TimeGenerator()
        seed(1)
        while(self.p1Made < self.part1Target or self.p2Made < self.part2Target or self.p3Made < self.part3Target):
            inspector1C1 = timeGenerator.getIns1() 
            
            rand = random()
            if(rand>0.5):
                print("Inspector 2 generate C2")
                inspector2C2 = timeGenerator.getIns22()
            else:
                print("Inspector 2 generate C2")
                inspector2C3 = timeGenerator.getIns23()
            

            


sim = simulation()
sim.sim()
            
