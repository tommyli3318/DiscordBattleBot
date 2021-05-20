import random
emoji = dict(Heal='🩹', Lightning='⚡', Sword='🗡️', Shield='🛡️')

class Duel:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.active_player = self.p1 # if random.random() > 0.5 else self.p2
        self.inactive_player = self.p2
    
    
    def attack(self):
        damage_dealt = round(self.active_player.base_damage * random.uniform(0.75, 1.25)) - self.inactive_player.armor
        crit = False
        if random.random() < self.active_player.crit:
            # crittical strike
            damage_dealt *= 2
            crit = True
        
        explanation = '```\nModifiers:\n'
        if 'Sword' in self.active_player.items:
            damage_dealt += 3
            explanation += "  +3 damage dealt from %s's Sword\n" % self.active_player.name
        if 'Shield' in self.inactive_player.items:
            damage_dealt -= 3
            explanation += "  -3 damage taken from %s's Shield\n" % self.inactive_player.name
        explanation += '```\n'
        
        self.inactive_player.health -= damage_dealt
        
        message = '%s attacked %s for %s ⚔️damage' % (self.active_player.name, self.inactive_player.name, damage_dealt)
        message += '_💥critical strike x2 damage_!\n' if crit else '\n'
        message += explanation
                
        if self.inactive_player.health <= 0: # game over
            return message + '🥳%s wins the duel🎉' % (self.active_player.name), True
        else:
            self.active_player, self.inactive_player = self.inactive_player, self.active_player
            return message + "%s's ❤️remaining health = %s\n%s's ❤️remaining health = %s\n\n\n**Start of %s's turn**\n" % (self.p1.name, self.p1.health, self.p2.name, self.p2.health, self.active_player.name), False
    
    
    def spell(self):
        # use spell
        message = '%s used %s\n' % (self.active_player.name, self.active_player.spell)
        
        if self.active_player.spell == 'Heal':
            self.active_player.health += 10
            message += '%s healed +10 ❤️health.\n' % self.active_player.name
        elif self.active_player.spell == 'Lightning':
            self.inactive_player.health -= 10
            message += '%s took 10 damage.\n' % self.inactive_player.name
        
        if self.inactive_player.health <= 0: # game over
            return message + '%s wins the duel.' % self.active_player.name, True
        else:
            self.active_player, self.inactive_player = self.inactive_player, self.active_player
            return message + "%s's ❤️remaining health = %s\n%s's ❤️remaining health = %s\n\n\n**Start of %s's turn**\n" % (self.p1.name, self.p1.health, self.p2.name, self.p2.health, self.active_player.name), False
    
    
    def both_players_picked(self):
        # check if both players have picked their spells and items
        return self.p1.spell and len(self.p1.items) == 1 and self.p2.spell and len(self.p2.items) == 1
    
    def get_stats(self):
        message = '```\n'
        message += "%s's stats:\n" % self.p1.name
        message += '  ❤️current health = %s\n' % self.p1.health
        message += '  ⚔️base damage = %s\n' % self.p1.base_damage
        message += '  🛡️armor = %s\n' % self.p1.armor
        message += '  💥critical strike chance = %s\n' % self.p1.crit
        if self.p1.spell:
            message += '  📖Spell = %s\n' % (emoji.get(self.p1.spell) + self.p1.spell)
        if self.p1.items:
            message += '  💰Items = %s\n' % ' '.join(emoji.get(item) + item for item in self.p1.items)
        message += '```\n'
        
        message += '```\n'
        message += "%s's stats:\n" % self.p2.name
        message += '  ❤️current health = %s\n' % self.p2.health
        message += '  ⚔️base damage = %s\n' % self.p2.base_damage
        message += '  🛡️armor = %s\n' % self.p2.armor
        message += '  💥critical strike chance = %s\n' % self.p2.crit
        if self.p2.spell:
            message += '  📖Spell = %s' % (emoji.get(self.p2.spell) + self.p2.spell)
        if self.p2.items:
            message += '  💰Items = %s' % ' '.join(emoji.get(item) + item for item in self.p2.items)
        message += '\n```'
        
        return message
