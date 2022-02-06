# Number generated based on assumption of normal distribution.
from scipy.stats import norm
class TimeGenerator():
    def __init__(self):
        self._avgInspector1 = 10.358
        self._avgInspector22 = 15.537
        self._avgInspector23 = 20.633
        self._avgWorkstation1 = 4.604
        self._avgWorkstation2 = 11.093
        self._avgWorkstation3 = 8.796
        self._SIGMA = 0.6
    
    def getIns1(self):
        ServiceTime = norm.rvs(loc = self._avgInspector1, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime

    def getIns22(self):
        ServiceTime = norm.rvs(loc = self._avgInspector22, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime
    
    def getIns23(self):
        ServiceTime = norm.rvs(loc = self._avgInspector23, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime
    
    def getWs1(self):
        ServiceTime = norm.rvs(loc = self._avgWorkstation1, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime

    def getWs2(self):
        ServiceTime = norm.rvs(loc = self._avgWorkstation2, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime

    def getWs3(self):
        ServiceTime = norm.rvs(loc = self._avgWorkstation3, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime
