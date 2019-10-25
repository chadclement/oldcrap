from evennia import default_cmds, utils
from evennia.contrib.rpsystem import ContribRPCharacter
import random
from random import randint
from evennia import TICKER_HANDLER as tickerhandler
import typeclasses.position as position
import typeclasses.magic as magic

############################################################
#                                                          #
#                      Skills:                             #
#             What ya gonna do about it?                   #
#                                                          #
#                                                          #
############################################################

def kick(self, target):
    if self.db.position is 1:
        self.msg("You can't fight while resting.")
        return
    #target = self.args.strip()
    if self.db.cooldown is True:
        self.msg("You are really tired.")
        return
    if not target or target == "me":
        self.msg("Use a valid target.")
        return
    else:
        #target = self.search(self.args.strip())
        target = self.search(target)
        if not target :
            return
        if target.account is self.account:
            self.msg("You try to kick yourself.")
            return
        
        self.db.cooldown = True
        cooldown = self.get_cooldown()
        self.check_health()
        target.db.health = round(target.db.health - (randint(1, 4) + (self.db.strength + self.db.offense) * .05))
        target.msg("{0} kicks you hard in the head!".format(self.db._sdesc))
        self.msg("Damn! You kicked {0}, dog.".format(target.db._sdesc.lower()))
    if target.db.health <= 0:
        self.msg("Your kick sends {0} to the realm of drov!".format(target.db._sdesc.lower()))        
    if target.db.position is 1:
        target.stand()
    target.check_health()
    utils.delay(cooldown, self.kick_cooldown)

def kick_cooldown(self):
    self.db.cooldown = False
    self.check_health()
    return