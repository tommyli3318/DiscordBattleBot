class Player:
    def __init__(self, name, base_damage=10):
        self.name = name
        
        self.health = 100
        self.base_damage = base_damage
        self.armor = 0
        
        self.lifesteal = 0
        self.crit = .05 # crit chance
        
        self.spell = None
        self.items = set()
