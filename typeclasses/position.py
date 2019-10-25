from evennia import default_cmds, utils
from random import randint
from evennia import TICKER_HANDLER as tickerhandler
from evennia.contrib.rpsystem import ContribRPCharacter

############################################################
#                                                          #
#                      Positions:                          #
#       0)  Standing                1)Resting              #
#       2)  Sleeping                3)Knocked out          #
#                                                          #
############################################################

def stand(self):
    if self.db.position is not 0:
        self.msg("You stand up.")
        for Character in self.location.contents:
            if Character is not self:
                Character.msg("{} stands up.".format(self.db._sdesc))    
        cooldown = (10 - (self.db.endurance * .1))
        tickerhandler.remove(cooldown, self.rest_tick)
        self.db.position = 0
    else:
        self.msg("You are already standing.")

def rest(self):
    if self.db.position is 1:
        self.msg("You are already resting.")
    else:
        for Character in self.location.contents:
            if Character is not self:
                Character.msg("{} rests.".format(self.db._sdesc))
        cooldown = (10 - (self.db.endurance * .1))
        self.msg("You sit down and rest.")
        self.db.position = 1
        tickerhandler.add(cooldown, self.rest_tick)


def rest_tick(self):
    cooldown = (10 - round(self.db.endurance * .1))
    if self.db.position is 1:
        if self.db.health < self.db.max_health and self.db.health > round(self.db.max_health * .3):
            self.db.health = (self.db.health + 1)
        if self.db.stamina < self.db.max_stamina:
            self.db.stamina = (self.db.stamina + 1)
        if self.db.magic < self.db.max_magic:
            self.db.magic = (self.db.magic + 1)
        self.msg("tick")
        self.check_health()
