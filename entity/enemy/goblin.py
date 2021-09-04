"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
Inherit from Enemy class, this class is for individual enemy object
"""

from entity.enemy.base import Enemy


class Goblin(Enemy):
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.base_attack = 5
        self.defense = 3
        self.magic = 5
        self.base_health = 200
        self.set_goblin_attribute()
        self.max_mana = 60
        self.max_health = self._get_max_health()
        self.health = self.max_health
        self.mana = self.max_mana
        self.skills = ['attack']
        self.exp = 20  # default experience points
        self.coin = 10  # default coins
    
    def fight(self, player):
        self.use_attack(player)
    
    def set_goblin_attribute(self):
        if self.name == 'Goblin Elite':
            self.base_attack = 10
            self.base_health = 300
            self.defense = 7
        elif self.name == 'Goblin Savage':
            self.base_attack = 20
            self.base_health = 420
            self.defense = 15