import numpy as np
from time import sleep
class Robot:
    def __init__(self,ActionDuration =0.01):
        self.actionduration = ActionDuration
        self.distance = np.random.randint(0,100)
        
    def RegulaizeSpeed(self,speed):
        if speed>255:
            return 255
        if speed<-255:
            return -255
        return speed
    
    def Move(self,speed):
        if speed ==0:
            self.StandStill()
        elif speed<0:
            self.bwd(speed)
        elif speed>0:
            self.fwd(speed)

    def fwd(self,speed):
        d = self.RegulaizeSpeed(speed) * self.actionduration
        self.distance-= d
        if self.distance<0:
            self.distance=0
        return self.distance
    
    def bwd(self,speed):
        
        d = -1*self.RegulaizeSpeed(speed) * self.actionduration
        self.distance+= d
        return self.distance
    
    def StandStill(self):
        sleep(self.actionduration)
        return self.distance
