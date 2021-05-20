class Player:
    def __init__(self, name, damage=10):
        self.name = name
        
        self.health = 100
        self.damage = damage
        self.armor = 0
        
        self.lifesteal = 0
        self.crit = .05 # crit chance
        
        self.spell = None
        self.items = set()
