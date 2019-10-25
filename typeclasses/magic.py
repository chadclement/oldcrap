from evennia import default_cmds, utils
from evennia.contrib.rpsystem import ContribRPCharacter
import random
from random import randint
from evennia import TICKER_HANDLER as tickerhandler
import typeclasses.position as position

############################################################
#                                                          #
#                      Magic:                              #
#                Yer a wizard Harry                        #
#                                                          #
#                                                          #
############################################################

def heal(self):
    if self.db.magic < 25:
        self.msg("You haven't the energy!")
        self.db.focus = False
        self.db.cooldown = False
        self.check_health()
        return
    else:
        self.db.magic = (self.db.magic - 25)
        for Character in self.location.contents:
            if Character is not self:
                Character.msg("A cool mist surrounds {}.".format(self.db._sdesc))
        self.db.health = (self.db.health + 40)
        if self.db.health > self.db.max_health:
            self.db.health = self.db.max_health
        self.msg("A warm feeling washes over you.")
        self.cast_cooldown()


def cast(self, spell):
    self.db.position = self.db.position
    if self.db.position is not 0:
        self.msg("You need to be standing.")
        return
    if self.db.focus is not True and self.db.cooldown is not True:
        self.msg("You begin to concentrate.")
        self.db.focus = True
        self.db.cooldown = True
        for Character in self.location.contents:
            if Character is not self:
                Character.msg("{0} begins to cast a spell".format(self.db._sdesc))
        if "fire" in spell:
            utils.delay(2, self.fire)
        if "heal" in spell:
            utils.delay(2, self.heal)            
    else:
        self.msg("You've already got too much on your mind!")
        return


def fire(self):
    self.msg("Flames erupt around you.")
    for Character in self.location.contents:
        if Character is not self:
            Character.msg("Flames erupt around {}.".format(self.db._sdesc))
    utils.delay(3, self.cast_cooldown)

def cast_cooldown(self):
    self.db.focus = False
    self.db.cooldown = False
    self.check_health()
    return
