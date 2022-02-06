from timeGenerator import TimeGenerator
import numpy as np
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
        while(self.p1Made < self.part1Target or self.p2Made < self.part2Target or self.p3Made < self.part3Target):
            inspector1Time = timeGenerator.getIns1()
            print(inspector1Time)


sim = simulation()
sim.sim()
            
