"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
Inherit from Enemy class, this class is for individual enemy object
"""

from entity.enemy.base import Enemy


class Savager(Enemy):
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.base_attack = 15
        self.defense = 5
        self.magic = 25
        self.base_health = 400
        self.max_mana = 60
        self.max_health = self._get_max_health()
        self.health = self.max_health
        self.mana = self.max_mana
        self.skills = ['attack', 'fireball']
        self.int = 15
        self.exp = 20  # default experience points
        self.coin = 10  # default coins
    
    def fight(self, player):
        if player.health * 100 / player.max_health > 75:
            self.use_fireball(player)
        else:
            self.use_attack(player)
