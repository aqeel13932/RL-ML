__author__ = 'aqeel'
from random import randint
from State import State

def DrawBlackCard():
    '''
    simulate draw a black card from (1-10) to use for the first draw
    :return:random integer from 1-10
    '''
    return randint(1,10)

def DrawCard():
    '''
    simulate draw a (red/black) from (1-10) card. with probability 1/3 for negative value and 2/3 for positive value
    :return:random integer from (-10 to 10)
    '''
    value = DrawBlackCard()

    #The Card might be red with probability 1/3
    if(randint(1,3)==1):
        value = value*-1
    return value

def CheckReward(s):
    '''
    :param s: Game State(type State)
    :return:signed integer as reward(-1,0,1))
    '''
    reward=0
    #The Game Ended Already(Someone Got Busted)
    if s.terminated:
        #The Player busted
        if s.PlayerBust:
            reward=-1
        #The Dealer busted
        else:
            reward=1
    #No one Got Busted
    else:
        #Player score is higher than the dealer
        if s.playersum>s.dealersum:
            reward=1
        #Dealer Score is higher than the player
        elif s.dealersum>s.playersum:
            reward=-1
        #Dealer and Player scores equal
        else:
            reward=0
    #Return
    return pow(s.BaseGamma,s.Playerdraws)*reward

def step(s,a):
    '''
    simulate the player single step, or dealer(all steps )
    :param s: the current state
    :param a: the action 0:hit ,1:stick
    :return: s' (the new  state ) and R ( the reward )
    '''
    if s.terminated:
        print 'Game Ended Already'
        return 0
    #Player is hitting
    if a==0:
        s.AddDrawnCardPlayer(DrawCard())
        return CheckReward(s)
    #The Player Stick , Dealer is hitting.
    elif a==1:
        #if game not terminated & the dealer sum is less than 17
        while not s.terminated and s.dealersum<17:
            s.AddDrawnCardDealer(DrawCard())
        return CheckReward(s)

def GetPlayerAction():
    action = raw_input('What do you want to do ? HIT:0 , STICK:1\n')
    return int(action)


print '---Game Started -----'
Easy21 = State(DrawBlackCard(),DrawBlackCard(),1)
print '---Inititation values ----'
print Easy21
action = GetPlayerAction()
while not Easy21.terminated:
    print 'reward:{:2d}'.format(step(Easy21,action)) , Easy21
    if action==1:
        break
    else:
        action=GetPlayerAction()




