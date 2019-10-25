"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
#from evennia import DefaultCharacter
from evennia import default_cmds, utils
from evennia.contrib.rpsystem import ContribRPCharacter
import random
from random import randint
from evennia import TICKER_HANDLER as tickerhandler
import typeclasses.position as position
import typeclasses.magic as magic
import typeclasses.skills as skills

class Character(ContribRPCharacter):
    def roll_stats(self):
        self.db.offense = random.randint(1,5)
        self.db.defense = random.randint(1,5)
        self.db.strength = random.randint(1,20)
        self.db.agility = random.randint(1,20)
        self.db.endurance = random.randint(1,20)
        self.db.wisdom = random.randint(1,20)
        self.db.max_health = random.randint(70,120)
        self.db.max_magic = random.randint(70,120)


    def at_object_creation(self):
        super().at_object_creation()
        self.db.offense = random.randint(1,20)
        self.db.defense = random.randint(1,20)
        self.db.strength = random.randint(1,20)
        self.db.agility = random.randint(1,20)
        self.db.endurance = random.randint(1,20)
        self.db.wisdom = random.randint(1,20)

        self.db.max_health = random.randint(70,120)
        self.db.health = self.db.max_health
        self.db.max_magic = random.randint(70,120)
        self.db.magic = self.db.max_magic
        self.db.max_stamina = random.randint(70,120)
        self.db.stamina = self.db.max_stamina
        self.db.max_stun = random.randint(70, 120)
        self.db.stun = self.db.max_stun

        self.db.position = 0
        self.db.is_poisoned = False
        self.db.dead = False
        self.db.config_color = False
        self.db.cooldown = False
        self.db.focus = False
        self.db.has_rerolled = False
    
    def cast(self, spell):
        magic.cast(self, spell)
    
    def cast_cooldown(self):
        magic.cast_cooldown(self)

    def heal(self):
        magic.heal(self)

    def kick(self, target):
        skills.kick(self, target)
    
    def kick_cooldown(self):
        skills.kick_cooldown(self)

    def rest(self):
        position.rest(self)

    def rest_tick(self):
        position.rest_tick(self)

    def stand(self):
        position.stand(self)
 
    def infobar(self):
        focus = ""
        is_poisoned = ""
        position_str = ""
        
        if self.db.position is 0:
            position_str = "Standing"
        if self.db.position is 1:
            position_str = "Resting"
        if self.db.cooldown is True:
            cooldown = "❌"
        if self.db.cooldown is False:
            cooldown = "✅"
        if self.db.focus is True:
            focus = "✨"
        if self.db.is_poisoned is True:
            is_poisoned = "💀"

        self.msg(prompt="{0}/{1} hp, {2}/{3} mp, {4}/{5} mv, Status:{6}{7}{8}| Position:{9}".format(self.db.health, self.db.max_health, self.db.magic, 
        self.db.max_magic, self.db.stamina, self.db.max_stamina, cooldown, focus, is_poisoned, position_str))
        return

    def score(self):
        strength, health, endurance, wisdom, agility, offense, magic, defense = self.get_abilities()
        string = "*** STR: %s, HP: %s, END: %s, WIS: %s, AGI: %s, OFF: %s, MP: %s, DEF: %s" % (
            strength, health, endurance, wisdom, agility, offense, magic, defense)
        self.msg("Your new stats\n" + string)
        return

    def get_abilities(self):
        return self.db.strength, self.db.max_health, self.db.endurance, self.db.wisdom, self.db.agility, self.db.offense, self.db.max_magic, 
        self.db.defense
    
    def get_cooldown(self):
        cooldown = round((7 / self.db.agility) + randint(3,4))
        self.msg("-- Cooldown of: {} ".format(cooldown))
        return cooldown

    def check_health(self):
        self.infobar()
        if self.db.health <= 0 : 
                self.msg("The last of your life leaves your body")
                self.delete()
        return

    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
