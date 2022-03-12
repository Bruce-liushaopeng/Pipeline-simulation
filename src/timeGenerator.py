import random
import numpy


class timeGenerator:
    def __init__(self, seed) -> None:
        random.seed(seed)

    def getIns1Time(self):
        MLE = 0.096545
        return self.generateTime(MLE)

    def getIns2Time(self):
        MLE = 0.064362
        return self.generateTime(MLE)

    def getIns3Time(self):
        MLE = 0.048466621
        return self.generateTime(MLE)

    def getWs1Time(self):
        MLE = 0.217182777

        return self.generateTime(MLE)

    def getWs2Time(self):
        MLE = 0.090150136

        return self.generateTime(MLE)

    def getWs3Time(self):
        MLE = 0.113693469

        return self.generateTime(MLE)

    def generateTime(self, mle):
        p = random.random()
        print(p)

        random_Time = numpy.log(1 - p) / (-mle)
        return random_Time
