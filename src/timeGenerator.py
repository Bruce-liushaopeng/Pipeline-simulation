import random
import numpy

class timeGenerator:
    def __init__(self,seed) -> None:
        random.seed(seed)
        self.seed = seed
    
    def getIns1Time(self):
        p = random.random()
        #print(p)
        MLE = 0.096545
        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time    
    
    def getIns2Time(self):
        p = random.random()
        #print(p)
        MLE = 0.064362
        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time  
    
    def getIns3Time(self):
        p = random.random()
        #print(p)
        MLE = 0.048466621
        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time  

    def getWs1Time(self):
        p = random.random()
        #print(p)
        MLE = 0.217182777
        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time  
    
    def getWs2Time(self):
        p = random.random()
        #print(p)
        MLE = 0.090150136

        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time  
    
    def getWs3Time(self):
        p = random.random()
        #print(p)
        MLE = 0.113693469

        ins1_time = numpy.log(1-p) / (-MLE)
        return ins1_time  

    def getSeed(self):
        return self.seed


