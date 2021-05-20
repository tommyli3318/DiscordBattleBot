import random

class Duel:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.active_player = self.p1 # if random.random() > 0.5 else self.p2
        self.inactive_player = self.p2
    
    
    def attack(self):
        damage_dealt = round(self.active_player.damage * random.uniform(0.75, 1.25)) - self.inactive_player.armor
        crit = False
        if random.random() < self.active_player.crit:
            # crittical strike
            damage_dealt *= 2
            crit = True
        
        self.inactive_player.health -= damage_dealt
        
        message = '%s attacked %s for %s damage' % (self.active_player.name, self.inactive_player.name, damage_dealt)
        message += '(critical strike)!\n' if crit else '\n'
                
        if self.inactive_player.health <= 0: # game over
            return message + '%s wins the duel.' % (self.active_player.name), True
        else:
            self.active_player, self.inactive_player = self.inactive_player, self.active_player
            return message + "%s's turn.\n%s's remaining health: %s\n%s's remaining health: %s" % (self.active_player.name, self.p1.name, self.p1.health, self.p2.name, self.p2.health), False
    
    
    def spell(self):
        # use spell
        message = '%s used %s\n' % (self.active_player.name, self.active_player.spell)
        
        if self.active_player.spell == 'Heal':
            self.active_player.health += 10
            message += '%s healed +10 health.\n' % self.active_player.name
        elif self.active_player.spell == 'Lightning':
            self.inactive_player.health -= 10
            message += '%s took 10 damage.\n' % self.inactive_player.name
        
        if self.inactive_player.health <= 0: # game over
            return message + '%s wins the duel.' % self.active_player.name, True
        else:
            self.active_player, self.inactive_player = self.inactive_player, self.active_player
            return message + "%s's turn.\n%s's remaining health: %s\n%s's remaining health: %s" % (self.active_player.name, self.p1.name, self.p1.health, self.p2.name, self.p2.health), False
    
    
    def both_players_picked(self):
        # check if both players have picked their spells and items
        return self.p1.spell and len(self.p1.items) == 1 and self.p2.spell and len(self.p2.items) == 1
