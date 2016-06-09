__author__ = 'aqeel'
from math import pow

#Class to represent the state.
class State:
    def __init__(self,dealercard,playercard,Gamma):
        '''
        :param dealercard: Dealer black card
        :param playercard: player black card
        :param Gamma: discount value
        '''
        # Total of dealer cards sum
        self.dealersum=dealercard

        # Total of Players cards
        self.playersum= playercard

        # Represent if someoe got busted
        self.terminated = False

        # No of Player draws
        self.Playerdraws=0

        # Player status
        self.PlayerBust=False

        # Dealer Status
        self.DealerBust=False

        # No of Dealer Draws
        self.Dealerdraws=0

        # discount value
        self.BaseGamma = Gamma

    def AddDrawnCardPlayer(self,value):
        '''
        add the drawn card value to player's sum and update the status of the game (ended or not ) & discount value
        :param value: signed integer from -10 to 10 represent the value and the color of the drawn card
        :return: Gamma for the current step
        '''
        if (self.terminated):
            print 'Game Ended Already'
        else:
            self.Playerdraws+=1
            self.playersum+=value
            if self.playersum>21 or self.playersum<1:
                self.terminated=True
                self.PlayerBust=True
                print 'The player lost.'

    def AddDrawnCardDealer(self,value):
        '''
        add the drawn card value to dealer's sum and update the status of the game (ended or not ) & discount value
        :param value: signed integer from -10 to 10 represent the value and the color of the drawn card
        :return: Gamma for the current step
        '''
        if (self.terminated):
            print 'Game Ended Already'
        else:
            self.Dealerdraws+=1
            self.dealersum+=value
            if self.dealersum>21 or self.dealersum<1:
                self.terminated=True
                self.DealerBust=True
                print 'The Dealer lost.'
            return pow(self.BaseGamma,self.Dealerdraws)

    def __str__(self):
        return 'Player Draws:{},Sum:{} ## Dealer Draws:{},Sum:{}'.format(self.Playerdraws,self.playersum,self.Dealerdraws,self.dealersum)