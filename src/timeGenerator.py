import random
import numpy

class timeGenerator:
    MLE_ins1 = 0.096545
    def __init__(self,seed) -> None:
        random.seed(seed)
    
    def getIns1Time(self):
        p = random.random()
        print(p)
        MLE = 0.096545
        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time    


