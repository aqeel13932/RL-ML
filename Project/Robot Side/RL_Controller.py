import numpy as np
from time import sleep
#from Driver import *
import Driver
class RL_Controller:
    
    def __init__(self,lmbda=0.1,optimal_distance=30,staticActionThreshould=1,actionscount=3,StatesCount=5,\
                 Exploration=0.1):
        '''
        staticActionThreshould : when distance more or less than 3*std Robot will get static action
        ActionsCount : 1 for no action , rest divided by 2 to cover positive , negative
        StatesCount : at least 4 per Side
        '''
        self.lmbda =lmbda
        self.Exploration = Exploration
        self.ActionsCount=actionscount
        self.StatesCount= StatesCount
        self.actions= 0
        self.States=0
        self.std = np.round(np.std(np.arange(0,optimal_distance*2)))*staticActionThreshould
        self.AcceptedError = np.array((-1.0,1.0))*(0.03*optimal_distance)
        self.qsa=0
        self.OptimalDistance =30
        np.random.seed(1377)
        #====Sarsa Related ===#
        self.qsa=0
        self.n=0
        self.et=0
        self.Terminated=False
        
        #self.stats = 
    def GenerateActions(self):
        if self.ActionsCount%2==0:
            self.ActionsCount+=1
        if self.ActionsCount<3:
            self.ActionsCount=3
        lst =[]
        #fwd or bwd number of actions
        for i in range ((self.ActionsCount-1)/2 +1):
            if i==0:
                lst.append(i)
                continue
            lst = [-i]+lst
            lst.append(i)
        self.actions= (np.array(lst)/(max(lst)*1.0))*255
        
    def GenerateStats(self):
        lst=[]
        if (self.StatesCount-1)%2==0:
            self.StatesCount+=1
        if self.StatesCount<4:
            self.StatesCount=4
        for i in range(self.StatesCount):
            if i==0:
                lst.append(i)
                continue
            lst = [-i]+lst
            lst.append(i)
        lst = (np.array(lst)/(np.max(lst)*1.0))*self.std
        lstdomains=[]
        for i in range(len(lst)-1):
            lstdomains.append((lst[i],lst[i+1]))
        lstdomains = [(-5000,lst[0])] + lstdomains
        lstdomains.append((lst[len(lst)-1],5000))
        self.States = np.array(lstdomains)
        self.StatesCount = self.States.shape[0]
    
    def PrepareForSarsa(self):
        self.qsa =np.random.uniform(-1,1,size=(self.States.shape[0],self.actions.shape[0]))
        self.et = np.zeros((self.States.shape[0],self.actions.shape[0]))
        self.n = np.zeros(self.States.shape[0])
        
    def Initalization(self):
        print '=====Initialization====='
        self.GenerateActions()
        self.GenerateStats()
        self.PrepareForSarsa()
        print """Lambda={},Exploration={},OptimalDistance={},Actions={},States={},Std={},Accepted Error={},Qsa={}""".\
        format(self.lmbda,self.Exploration,self.OptimalDistance,self.actions.shape,self.States.shape,self.std,\
               self.AcceptedError,self.qsa.shape)
        
    def GetStateIndex(self,CurrentState):
        for i in range (self.States.shape[0]):
            if self.States[i,0]<=CurrentState<=self.States[i,1]:
                return i
    
    def GetAction(self,statindx):
        
        #Deterministic solution for state out of range to assure the Robot won't get lost
        if statindx==0:
            #print 'distance:{},statindx:{},state:{},action:{}'.format(self.Robot.distance, statindx,self.States[statindx],self.actions[len(self.actions)-1])
            return 0
        if statindx==len(self.States)-1:
            #print 'distance:{},statindx:{},state:{},action:{}'.format(self.Robot.distance,statindx,self.States[statindx],self.actions[0])
            return len(self.actions)-1
        #Exploration Precentage depend on how many specific state  visited
        exploration = 100.0 / (100.0 + self.n[statindx])
        rnd = np.random.rand()
        if rnd < exploration:
            rnd = np.random.randint(len(self.actions))
            return rnd
        else:
            return np.argmax(self.qsa[statindx])
        
    def Step(self,actnindx):
        self.Robot.Move(self.actions[actnindx])
        crntstat = self.GetCurrentState()
        return crntstat,self.GetReward(crntstat)
    
    def GetCurrentState(self):
        return self.Robot.distance - self.OptimalDistance
    
    def GetReward(self,crntstat):
        if self.AcceptedError[0]<=crntstat<=self.AcceptedError[1]:
            self.Terminated=True
            return 1000;
        else:
            return crntstat if crntstat<0 else -1*crntstat
    def UpdateQsa(self,s_indx,s_pindx,a_indx,a_pindx,R):
        self.n[s_indx] += 1
        if self.Terminated:
            qnext =0
        else:
            qnext = self.qsa[s_pindx,a_pindx]

        delta = R + qnext - self.qsa[s_indx,a_indx]
        self.et[s_indx,a_indx] += 1
        try:
            alpha = 1.0 / self.n[s_indx]
        except:
            alpha = 0

        self.qsa += alpha * delta * self.et
        self.et *= self.lmbda
        
    def PlaySarasa(self,nepisode):
        self.n.fill(0)
        for i in range(nepisode):
            self.et.fill(0)
            self.Robot=Robot()
            #print self.Robot.distance
            self.Terminated=False
            #---Game Started -----#
            s = self.GetCurrentState()
            sindx = self.GetStateIndex(s)
            aindx = self.GetAction(sindx)
            iit=0
            while not self.Terminated:
                iit+=1
                s_p, R = self.Step(aindx)
                s_pindx = self.GetStateIndex(s)
                a_pindx = self.GetAction(s_pindx)
                #if i==3 :
                #    print 'dist={},new State = {},s_pindx={},Reward {},new Action = {}'\
                #    .format(self.Robot.distance, s_p,s_pindx,R,self.actions[a_pindx])
                #    if iit==100:
                #        self.Terminated=True
                self.UpdateQsa(sindx,s_pindx,aindx,a_pindx,R)
                s = s_p
                sindx = s_pindx
                aindx = a_pindx
                
                #action= GetPlayerAction(Easy21)
                #Update Qsa
                #Update(oldp-1,oldd-1,olda,Easy21.Reward,Easy21.playersum-1,action,Easy21.terminated)
                #if Easy21.terminated:
                #    break
                #if i%10000==0:
                #    print i
            if i%10000==0:
                print 'Episode :{}'.format(i)
        self.SaveModel(nepisode)
    def Play(self,episods):
		self.LoadModel(episods)
		try:
                    while 10:
                            s =   Driver.ReadAverage() - self.OptimalDistance
                            sindx = self.GetStateIndex(s)
                            aindx = self.GetAction(sindx)
                            Driver.Move(self.actions[aindx])
		except:
			Driver.StopEveryThing()
    def SaveModel(self,episods,name='qsa'):
        fname = '{},stc:{},ac:{},epi:{}.dat'.format(name,self.States.shape[0],self.actions.shape[0],episods)
        self.qsa.dump(fname)
        
    def LoadModel(self,episods,name='qsa'):
        fname = '{},stc:{},ac:{},epi:{}.dat'.format(name,self.States.shape[0],self.actions.shape[0],episods)
        self.qsa = np.load(fname)
           #for i,__ in np.ndenumerate(qsa):
               #print i
        
            

main = RL_Controller(optimal_distance=30,actionscount=10,StatesCount=40)
main.Initalization()
main.Play(30000)
